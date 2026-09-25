from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
import os
from dotenv import load_dotenv

# Load environment variables (like GROQ_API_KEY) from .env file
load_dotenv()

from langgraph.checkpoint.memory import MemorySaver
from graph.workflow import workflow

app = FastAPI(title="Agentic Clinical Copilot API", description="LangGraph Orchestrated Clinical Deterioration System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup LangGraph Checkpointer 
# Using MemorySaver for this local prototype; in production, use SqliteSaver or PostgresSaver.
memory = MemorySaver()

# Compile the graph! 
# We explicitly pause execution right before 'human_in_loop' so a doctor can review.
app_graph = workflow.compile(
    checkpointer=memory,
    interrupt_before=["human_in_loop"]
)

class VitalsReading(BaseModel):
    patient_id: str
    heart_rate_bpm: float
    spo2_percent: float
    respiratory_rate_bpm: float
    systolic_bp_mmhg: float
    diastolic_bp_mmhg: float

class ClinicianDecision(BaseModel):
    decision: str  # accept, dismiss, defer, investigate
    clinician_id: str

@app.post("/vitals/stream")
def ingest_vitals(reading: VitalsReading):
    """
    Ingests a single reading and pushes it into the patient's LangGraph thread.
    """
    thread = {"configurable": {"thread_id": reading.patient_id}}
    
    # Retrieve existing state to append to the buffer
    current_state = app_graph.get_state(thread)
    
    if current_state.values:
        vitals_buffer = current_state.values.get("vitals_buffer", [])
    else:
        vitals_buffer = []
        
    vitals_buffer.append(reading.model_dump())
    
    # Check if currently paused waiting for human-in-loop
    if current_state.next and "human_in_loop" in current_state.next:
        # Don't push new state if we are waiting for a doctor's decision.
        # Just return the existing alert data.
        return {
            "status": "paused",
            "patient_id": reading.patient_id,
            "requires_human_review": True,
            "escalation_data": current_state.values.get("escalation")
        }

    # Push the event through the StateGraph
    result = app_graph.invoke(
        {"vitals_buffer": vitals_buffer, "patient_id": reading.patient_id}, 
        config=thread
    )
    
    # Check if the graph paused because it escalated an alert
    current_state_after = app_graph.get_state(thread)
    is_paused = "human_in_loop" in current_state_after.next
    
    return {
        "status": "ingested", 
        "patient_id": reading.patient_id, 
        "alerts_count": len(result.get("active_alerts", [])),
        "escalation_available": result.get("escalation") is not None,
        "escalation_data": result.get("escalation"),
        "requires_human_review": is_paused
    }

@app.get("/api/simulate/data")
def get_simulation_data():
    """Reads the local vitals_stream.csv and serves it to the frontend simulator."""
    import csv
    data = []
    try:
        with open("vitals_stream.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append({
                    "patient_id": row["patient_id"],
                    "timestamp": row["timestamp"],
                    "heart_rate_bpm": float(row["heart_rate_bpm"]) if row.get("heart_rate_bpm") else 0.0,
                    "spo2_percent": float(row["spo2_percent"]) if row.get("spo2_percent") else 0.0,
                    "respiratory_rate_bpm": float(row["respiratory_rate_bpm"]) if row.get("respiratory_rate_bpm") else 0.0,
                    "systolic_bp_mmhg": float(row["systolic_bp_mmhg"]) if row.get("systolic_bp_mmhg") else 0.0,
                    "diastolic_bp_mmhg": float(row["diastolic_bp_mmhg"]) if row.get("diastolic_bp_mmhg") else 0.0,
                })
    except Exception as e:
        print("Error reading CSV:", e)
    return data

@app.get("/alerts/priority-queue")
def get_priority_queue():
    """
    Fetches the active priority queue.
    In a full DB-backed deployment, this queries the Postgres/SQLite view.
    """
    return {"message": "Priority queue endpoint ready."}

@app.post("/alerts/{patient_id}/decision")
def submit_decision(patient_id: str, decision: ClinicianDecision):
    """
    Resumes a paused LangGraph thread waiting at the human_in_loop node.
    """
    thread = {"configurable": {"thread_id": patient_id}}
    state = app_graph.get_state(thread)
    
    if not state.next or "human_in_loop" not in state.next:
        raise HTTPException(status_code=400, detail="Graph is not currently paused waiting for a human decision.")
        
    # Inject the clinician's decision into the graph state
    decision_payload = decision.model_dump()
    app_graph.update_state(thread, {"clinician_decision": decision_payload}, as_node="human_in_loop")
    
    # Resume the graph (which will step to audit_log_write, then END)
    final_result = app_graph.invoke(None, config=thread)
    
    return {
        "status": "decision_recorded", 
        "audit_log_updated": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
