import os
import json
import sqlite3
import pandas as pd
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from the .env file located next to agent.py
_env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=_env_path, override=True)
print("Loaded GEMINI_API_KEY:", os.getenv("GEMINI_API_KEY"))

# We only import antigravity if the key exists to prevent crashing if it's not installed/configured properly
try:
    from google.antigravity import Agent, LocalAgentConfig
    AG_AVAILABLE = True
except ImportError:
    AG_AVAILABLE = False

DB_NAME = "copilot.db"

# --- Structured Output Schema ---
class RecommendationOutput(BaseModel):
    patient_id: str = Field(description="The ID of the patient")
    alert_level: str = Field(description="The severity level of the alert (e.g., Critical, High)")
    summary: str = Field(description="A 1-2 sentence summary of the deterioration event")
    detected_signals: List[str] = Field(description="The specific vital signs that triggered the alert")
    evidence: str = Field(description="The specific recent vital readings that support the recommendation")
    patient_context: str = Field(description="Relevant medical history, age, or medications that increase risk")
    protocol_source: str = Field(description="The ID or name of the clinical protocol retrieved and consulted")
    recommendation: str = Field(description="The concise, evidence-grounded clinical decision-support recommendation")
    limitations: str = Field(description="Any limitations in the data or explicitly stating that clinician assessment is required")

# --- Agent Tools ---

def get_patient_context(patient_id: str) -> str:
    """Retrieves the patient's age, relevant medical history, current medications, and most recent available labs.
    
    Args:
        patient_id: The ID of the patient to look up (e.g., 'P-001')
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT age, history, medications, recent_labs FROM patients WHERE patient_id = ?", (patient_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return f"Error: Patient {patient_id} not found in database."
            
        history = ", ".join(json.loads(row[1])) if row[1] else "None"
        meds = ", ".join(json.loads(row[2])) if row[2] else "None"
        
        return (
            f"Patient Context for {patient_id}:\n"
            f"- Age: {row[0]}\n"
            f"- Medical History: {history}\n"
            f"- Medications: {meds}\n"
            f"- Recent Labs: {row[3]}\n"
        )
    except Exception as e:
        return f"Error retrieving patient context: {str(e)}"


def get_vital_history(patient_id: str) -> str:
    """Retrieves the most recent 10 vital observations for the patient.
    
    Args:
        patient_id: The ID of the patient to look up.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query(
            f"SELECT timestamp, heart_rate_bpm, spo2_percent, respiratory_rate_bpm, systolic_bp_mmhg, diastolic_bp_mmhg "
            f"FROM vital_readings WHERE patient_id = '{patient_id}' ORDER BY timestamp DESC LIMIT 10", 
            conn
        )
        conn.close()
        
        if df.empty:
            return f"No vital history found for {patient_id}."
            
        # Reverse to be in chronological order
        df = df.iloc[::-1]
        
        return f"Recent Vital History for {patient_id} (Chronological):\n{df.to_string(index=False)}"
    except Exception as e:
        return f"Error retrieving vital history: {str(e)}"


def get_clinical_protocol(signals: str) -> str:
    """Retrieves the relevant clinical protocol/guideline based on the detected deterioration signals.
    
    Args:
        signals: A string describing the concerning signals (e.g., 'spo2_percent respiratory_rate_bpm')
    """
    try:
        from retrieval import ProtocolRetriever
        retriever = ProtocolRetriever()
        
        # Clean the signals for better TF-IDF matching (e.g., spo2_percent -> spo2 percent)
        clean_signals = signals.replace("_", " ").replace("bpm", "").replace("mmhg", "").strip()
        match = retriever.find_protocol(clean_signals)
        
        if not match:
            return "No matching protocol found in the knowledge base."
            
        return (
            f"Retrieved Protocol Document ID: {match['document_id']}\n"
            f"Section: {match['section_title']}\n\n"
            f"Protocol Text:\n{match['text_excerpt']}\n"
        )
    except Exception as e:
        return f"Error retrieving protocol: {str(e)}"

# --- Main Agent Wrapper ---

class ClinicalEscalationAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.is_available = bool(self.api_key) and AG_AVAILABLE
        
        if self.is_available:
            system_instruction = (
                "You are a clinical decision-support copilot. "
                "Your role is to help a clinician interpret a detected deterioration event using ONLY the evidence supplied through the available tools.\n\n"
                "Rules:\n"
                "- Do not invent patient information.\n"
                "- Do not invent vital readings.\n"
                "- Do not invent laboratory results.\n"
                "- Do not invent clinical protocols.\n"
                "- Do not claim to have retrieved information that was not retrieved.\n"
                "- Clearly distinguish observed data from interpretation.\n"
                "- Ground recommendations in the retrieved patient context, vital history, detected deterioration signals, and retrieved protocol.\n"
                "- Do not diagnose autonomously.\n"
                "- Do not prescribe medication.\n"
                "- Do not issue autonomous treatment orders.\n"
                "- Recommend clinician review/escalation according to the retrieved protocol when appropriate.\n"
                "- If evidence is insufficient, explicitly state that more information or clinician assessment is required.\n"
                "- Keep recommendations concise and understandable to a clinician.\n\n"
                "You MUST use all three tools to investigate the patient before generating your final response."
            )
            
            self.config = LocalAgentConfig(
                api_key=self.api_key,
                system_instructions=system_instruction,
                tools=[get_patient_context, get_vital_history, get_clinical_protocol],
                response_schema=RecommendationOutput
            )

    async def generate_recommendation(self, patient_id: str, alert_score: float, concerning_signals: List[str]) -> dict:
        """
        Invokes the agent to generate a recommendation. 
        Returns a dict matching RecommendationOutput schema, or a fallback dict if LLM fails.
        """
        fallback_response = {
            "patient_id": patient_id,
            "alert_level": "High" if alert_score < 10 else "Critical",
            "summary": "System detected multi-signal deterioration.",
            "detected_signals": concerning_signals,
            "evidence": "See vital history chart.",
            "patient_context": "Unavailable (Agent Fallback)",
            "protocol_source": "System Fallback",
            "recommendation": f"SYSTEM FALLBACK: Review patient promptly. Deterioration detected in: {', '.join(concerning_signals)}.",
            "limitations": "AI Agent unavailable. Recommendation is auto-generated by fallback system."
        }
        
        if not self.is_available:
            return fallback_response

        try:
            prompt = (
                f"A potential deterioration event has been triggered for patient {patient_id}.\n"
                f"The alerting system assigned a priority score of {alert_score}.\n"
                f"The concerning signals detected are: {', '.join(concerning_signals)}.\n"
                f"Please investigate using your tools and provide an evidence-grounded recommendation."
            )
            
            async with Agent(self.config) as agent:
                response = await agent.chat(prompt)
                
                # Use the correct SDK method for structured Pydantic output
                result = await response.structured_output()
                
                if result is None:
                    print("Agent returned None structured output.")
                    return fallback_response
                
                # result is already a dict matching RecommendationOutput schema
                return result
                    
        except Exception as e:
            print(f"Agent Execution Error: {str(e)}")
            return fallback_response
