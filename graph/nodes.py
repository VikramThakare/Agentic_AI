import os
import json
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from state.schema import PatientState
from rag.retriever import retrieve_protocol_evidence

# Pydantic schema for LangChain's Structured Output parsing
class ClinicalRecommendation(BaseModel):
    risk_score: float = Field(description="Computed risk score from 1.0 to 10.0")
    severity_tier: str = Field(description="watch, warning, or critical")
    triggering_signals: list[str] = Field(description="The vital signs that triggered this alert")
    plain_language_explanation: str = Field(description="A clear, short explanation for the clinician")
    recommended_actions: list[str] = Field(description="Specific actionable steps extracted strictly from the retrieved protocol")
    evidence_citations: list[str] = Field(description="Quotes or section titles from the retrieved protocol to ground the recommendation")

def ingest_reading_node(state: PatientState):
    """Enforces the rolling buffer window (last 30 readings roughly equal to 30 mins)."""
    buffer = state.get("vitals_buffer", [])
    state["vitals_buffer"] = buffer[-30:]
    return state

import csv

def update_profile_node(state: PatientState):
    """Placeholder: Calculates delta / mean over rolling window and fetches static context."""
    # Fetch patient history from CSV
    if not state.get("static_context"):
        patient_id = state.get("patient_id")
        # Try reading from patients.csv (in a real app, this would be a DB query)
        try:
            with open("patients.csv", "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("patient_id") == patient_id:
                        state["static_context"] = {
                            "age": row.get("age", ""),
                            "history": row.get("history", ""),
                            "medications": row.get("medications", "")
                        }
                        break
        except Exception as e:
            print("Failed to load patient static context:", e)
    return state

def detect_trend_node(state: PatientState):
    """
    Rule engine detecting persistence across readings.
    Sets severity tiers and appends to active_alerts if condition persists.
    """
    buffer = state.get("vitals_buffer", [])
    alerts = state.get("active_alerts", [])
    static_context = state.get("static_context", {})
    
    # Tick counter to evaluate every 10 seconds
    ticks = static_context.get("eval_ticks", 0) + 1
    static_context["eval_ticks"] = ticks
    state["static_context"] = static_context
    history = str(static_context.get("history", "")).lower()
    
    # We require at least 3 readings for persistence, but evaluate every 10 ticks
    if len(buffer) >= 3 and ticks % 10 == 0:
        latest = buffer[-1]
        
        # Dynamic Thresholds based on patient history
        spo2_threshold = 88 if ("copd" in history or "asthma" in history) else 92
        sys_bp_low = 90
        hr_high = 120
        
        # Example logic for Respiratory
        if latest.get("spo2_percent", 100) < spo2_threshold and latest.get("respiratory_rate_bpm", 15) > 22:
            alerts.append({
                "alert_id": f"AL-RESP-{datetime.now().timestamp()}",
                "category": "respiratory",
                "severity_tier": "critical",
                "triggering_signals": ["spo2_percent", "respiratory_rate_bpm"],
                "first_fired_at": datetime.now().isoformat(),
                "last_fired_at": datetime.now().isoformat()
            })
            
        # Example logic for Cardiovascular
        elif latest.get("heart_rate_bpm", 70) > hr_high and latest.get("systolic_bp_mmhg", 120) < sys_bp_low:
            alerts.append({
                "alert_id": f"AL-CARD-{datetime.now().timestamp()}",
                "category": "cardiovascular",
                "severity_tier": "critical",
                "triggering_signals": ["heart_rate_bpm", "systolic_bp_mmhg"],
                "first_fired_at": datetime.now().isoformat(),
                "last_fired_at": datetime.now().isoformat()
            })
            
    state["active_alerts"] = alerts
    return state

def retrieve_evidence_node(state: PatientState):
    """Retrieves chunks from Chroma DB matching the triggered alert's category."""
    alerts = state.get("active_alerts", [])
    if not alerts:
        return state
        
    latest_alert = alerts[-1]
    category = latest_alert["category"]
    signals = " and ".join(latest_alert["triggering_signals"])
    
    # Retrieve exactly from the matched protocol
    docs = retrieve_protocol_evidence(query=signals, category=category, k=3)
    
    evidence_text = "\n\n".join([f"--- Source: {d.metadata.get('source', 'Unknown')} ---\n{d.page_content}" for d in docs])
    state["retrieved_evidence"] = evidence_text
    return state

def reason_generate_node(state: PatientState):
    """
    Calls ChatGroq (Llama 3.3 70B) to reason over the vitals + evidence.
    Returns structured Pydantic output.
    """
    llm = ChatOpenAI(
        model="openrouter/free",
        api_key=os.getenv("OPENROUTER_API_KEY", ""),
        base_url="https://openrouter.ai/api/v1",
        temperature=0
    )
    
    parser = PydanticOutputParser(pydantic_object=ClinicalRecommendation)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert clinical AI copilot. Given the patient's vitals, medical history, and retrieved protocol evidence, output a highly accurate clinical recommendation. Do not hallucinate outside the provided protocol evidence. Always consider the patient's medical history when recommending actions. YOU MUST ALWAYS PROVIDE AT LEAST ONE SPECIFIC ACTIONABLE STEP in the `recommended_actions` array.\n\n{format_instructions}"),
        ("human", "Patient History: {history}\n\nPatient Vitals (Last 30 secs): {vitals}\n\nAlert Details: {alerts}\n\nRetrieved Protocol Evidence:\n{evidence}")
    ])
    
    chain = prompt | llm | parser
    
    vitals_str = json.dumps(state.get("vitals_buffer", [])[-30:])
    alerts_str = json.dumps(state.get("active_alerts", [])[-1:] if state.get("active_alerts") else [])
    evidence_str = state.get("retrieved_evidence", "No evidence retrieved.")
    
    history_str = json.dumps(state.get("static_context", {}))
    
    try:
        recommendation = chain.invoke({
            "history": history_str,
            "vitals": vitals_str,
            "alerts": alerts_str,
            "evidence": evidence_str,
            "format_instructions": parser.get_format_instructions()
        })
        state["escalation"] = recommendation.model_dump() # dict, not json string
    except Exception as e:
        state["escalation"] = {"error": f"LLM Generation failed: {str(e)}"}
        
    return state

def human_in_loop_node(state: PatientState):
    """LangGraph pause point for clinician approval."""
    return state

def audit_log_write_node(state: PatientState):
    """Appends an audit log entry for this graph cycle."""
    log = state.get("audit_log", [])
    log.append({
        "timestamp": datetime.now().isoformat(), 
        "action": "graph_cycle_complete",
        "alert_count": len(state.get("active_alerts", []))
    })
    state["audit_log"] = log
    return state
