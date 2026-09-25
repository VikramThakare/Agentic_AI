from typing import TypedDict, List, Dict, Any, Optional
from datetime import datetime

class Alert(TypedDict):
    alert_id: str
    category: str
    severity_tier: str  # watch, warning, critical
    triggering_signals: List[str]
    first_fired_at: str
    last_fired_at: str

class PatientState(TypedDict):
    """
    LangGraph state schema for a single patient's continuous monitoring loop.
    thread_id in LangGraph should map to the patient_id.
    """
    patient_id: str
    
    # Static Context
    static_context: Dict[str, Any]  # age, history, meds, last labs
    
    # Dynamic Vitals Buffer (rolling window of last N readings)
    vitals_buffer: List[Dict[str, Any]]
    
    # Current computed scores (qSOFA, SIRS, NEWS2-style)
    current_scores: Dict[str, float]
    
    # Active/Historical alerts
    active_alerts: List[Alert]
    
    # RAG retrieved evidence for current reasoning pass
    retrieved_evidence: str
    
    # Generated recommendation by LLM
    escalation: str
    
    # Clinician Decision state
    clinician_decision: Optional[Dict[str, Any]]  # decision (accept/dismiss), timestamp, clinician_id
    
    # Audit trail for the current cycle
    audit_log: List[Dict[str, Any]]
