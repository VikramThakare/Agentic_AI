import os
import json
from datetime import datetime
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
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

def update_profile_node(state: PatientState):
    """Placeholder: Calculates delta / mean over rolling window."""
    return state

def detect_trend_node(state: PatientState):
    """
    Rule engine detecting persistence across readings.
    Sets severity tiers and appends to active_alerts if condition persists.
    """
    buffer = state.get("vitals_buffer", [])
    alerts = state.get("active_alerts", [])
    
    # We require at least 3 readings for persistence (per requirements)
    if len(buffer) >= 3:
        latest = buffer[-1]
        
        # Example logic for Respiratory
        if latest.get("spo2_percent", 100) < 92 and latest.get("respiratory_rate_bpm", 15) > 22:
            alerts.append({
                "alert_id": f"AL-RESP-{datetime.now().timestamp()}",
                "category": "respiratory",
                "severity_tier": "critical",
                "triggering_signals": ["spo2_percent", "respiratory_rate_bpm"],
                "first_fired_at": datetime.now().isoformat(),
                "last_fired_at": datetime.now().isoformat()
            })
            
        # Example logic for Cardiovascular
        elif latest.get("heart_rate_bpm", 70) > 120 and latest.get("systolic_bp_mmhg", 120) < 90:
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
    llm = ChatGroq(
        temperature=0, 
        model_name="qwen/qwen3.8-27b",
        api_key=os.getenv("GROQ_API_KEY", "")
    )
    
    # Bind the LLM to output our exact Pydantic schema
    structured_llm = llm.with_structured_output(ClinicalRecommendation)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert clinical AI copilot. Given the patient's vitals, background, and retrieved protocol evidence, output a highly accurate clinical recommendation. Do not hallucinate outside the provided protocol evidence."),
        ("human", "Patient Vitals (Last 3 mins): {vitals}\n\nAlert Details: {alerts}\n\nRetrieved Protocol Evidence:\n{evidence}")
    ])
    
    chain = prompt | structured_llm
    
    vitals_str = json.dumps(state.get("vitals_buffer", [])[-3:])
    alerts_str = json.dumps(state.get("active_alerts", [])[-1:] if state.get("active_alerts") else [])
    evidence_str = state.get("retrieved_evidence", "No evidence retrieved.")
    
    try:
        # Generate the structured recommendation
        recommendation = chain.invoke({
            "vitals": vitals_str,
            "alerts": alerts_str,
            "evidence": evidence_str
        })
        state["escalation"] = recommendation.model_dump_json()
    except Exception as e:
        state["escalation"] = json.dumps({"error": f"LLM Generation failed: {str(e)}"})
        
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
