from langgraph.graph import StateGraph, END
from state.schema import PatientState
from graph.nodes import (
    ingest_reading_node,
    update_profile_node,
    detect_trend_node,
    retrieve_evidence_node,
    reason_generate_node,
    human_in_loop_node,
    audit_log_write_node
)

# --- Conditional Edges ---

def route_after_trend_detection(state: PatientState) -> str:
    """
    If no trend detected or alert is suppressed, route to audit_log_write (skip LLM).
    If a NEW or ESCALATED trend is detected, route to retrieve_evidence.
    """
    alerts = state.get("active_alerts", [])
    # Placeholder logic: Check if there's a severe alert requiring LLM reasoning
    if alerts and any(a.get("severity_tier") in ["warning", "critical"] for a in alerts):
        return "retrieve_evidence"
    return "audit_log_write"  # End this cycle without LLM call to save cost

# --- Build the StateGraph ---

workflow = StateGraph(PatientState)

# 1. Add Nodes
workflow.add_node("ingest_reading", ingest_reading_node)
workflow.add_node("update_profile", update_profile_node)
workflow.add_node("detect_trend", detect_trend_node)
workflow.add_node("retrieve_evidence", retrieve_evidence_node)
workflow.add_node("reason_generate", reason_generate_node)
workflow.add_node("human_in_loop", human_in_loop_node)
workflow.add_node("audit_log_write", audit_log_write_node)

# 2. Add Standard Edges
workflow.set_entry_point("ingest_reading")
workflow.add_edge("ingest_reading", "update_profile")
workflow.add_edge("update_profile", "detect_trend")

# 3. Add Conditional Routing
workflow.add_conditional_edges(
    "detect_trend",
    route_after_trend_detection,
    {
        "retrieve_evidence": "retrieve_evidence",
        "audit_log_write": "audit_log_write" # Skip LLM
    }
)

workflow.add_edge("retrieve_evidence", "reason_generate")
workflow.add_edge("reason_generate", "human_in_loop")
workflow.add_edge("human_in_loop", "audit_log_write")
workflow.add_edge("audit_log_write", END)

# We leave compilation (with the SqliteSaver checkpointer) for Phase 4 inside the API layer.
# app_graph = workflow.compile(...)
