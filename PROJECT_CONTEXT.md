# PROJECT_CONTEXT.md — Handoff Document

**Project**: Agentic Clinical Deterioration & Escalation Copilot (LangGraph Architecture)
**Last Updated**: 2026-09-25
**Disclaimer**: Educational prototype only. Not a medical device. Not for clinical use.

---

## 1. Project Overview & Objective

This is a prototype clinical decision-support system that monitors a simulated real-time stream of patient vital signs. It maintains per-patient state, detects multi-parameter deterioration trends, and escalates genuine persistent cases to a clinician with an **AI-generated, evidence-grounded recommendation** powered by the Groq API (using `qwen/qwen3.8-27b`).

The core engine has been upgraded to use **LangGraph** as a state machine. The workflow triggers a RAG pipeline to pull relevant clinical protocols, generates a structured LLM recommendation, and strictly enforces a **Human-in-the-Loop (HITL)** pause. The graph halts execution until a clinician explicitly approves or dismisses the generated protocol via the UI.

---

## 2. Current Project Status

**All core agentic and architectural milestones are COMPLETE:**
- ✅ Vanilla HTML/CSS/JS Frontend Dashboard with infinite synthetic vitals stream.
- ✅ FastAPI Backend to handle real-time streaming endpoints.
- ✅ LangGraph `StateGraph` definition and execution (`workflow.py`).
- ✅ Rolling buffer management for vital readings inside the graph state.
- ✅ TF-IDF RAG retrieval system integrated directly into LangGraph nodes.
- ✅ Groq-powered LLM reasoning node with structured JSON output.
- ✅ Beautiful UI parsing of the LLM JSON response.
- ✅ **Human-in-the-Loop** pause: LangGraph suspends execution and ignores new vitals for that patient until the clinician acts.
- ✅ Clinician Action API (`/alerts/{patient_id}/decision`) to resume the graph.

---

## 3. Folder/File Structure

```
AgeniAi/
├── .env                          # API key (GROQ_API_KEY)
├── README.md                     # Project overview and setup instructions
├── requirements.txt              # Python dependencies
│
├── api/
│   └── server.py                 # FastAPI server, compiles and executes LangGraph
│
├── frontend/
│   ├── index.html                # Real-time dashboard UI
│   ├── app.js                    # Synthetic stream generator and UI logic
│   └── styles.css                # CSS styling
│
├── graph/
│   ├── workflow.py               # Defines the LangGraph StateGraph and edges
│   └── nodes.py                  # Defines the logic for each graph node
│
├── state/
│   └── schema.py                 # Defines the PatientState TypedDict
│
├── data/
│   └── protocols/                # Markdown files used for RAG
│
└── ingestion.py                  # Legacy data ingestion script
```

---

## 4. Purpose of Every Important File

| File | Purpose |
|------|---------|
| `api/server.py` | FastAPI application. Instantiates the LangGraph with a MemorySaver checkpointer. Defines endpoints for `/vitals/stream` (invokes graph) and `/alerts/{patient_id}/decision` (resumes graph). Evaluates if the graph is paused before injecting new vitals. |
| `graph/workflow.py` | Connects the nodes: `ingest_reading` -> `update_profile` -> `detect_trend` -> [conditional: `retrieve_evidence` or `audit_log`] -> `reason_generate` -> `human_in_loop` -> `audit_log_write`. |
| `graph/nodes.py` | Contains the actual business logic for each node. `detect_trend_node` checks the rolling buffer for thresholds (e.g. SpO2 < 92 and RR > 22). `retrieve_evidence_node` does TF-IDF RAG. `reason_generate_node` calls ChatGroq. |
| `frontend/app.js` | Generates continuous random walk vital signs for 5 patients every 1 second (representing 1 minute in real time). Every 30 seconds, it globally flushes the alerts board. Intercepts `escalation_available` from the API and beautifully formats the JSON output into a UI card with Action buttons. |
| `frontend/index.html` | The HTML layout for the dashboard. |

---

## 5. Important Technical Decisions

1. **LangGraph Migration**: We moved from a static loop to a LangGraph `StateGraph`. This allows us to leverage built-in checkpointers for the `interrupt_before=["human_in_loop"]` functionality, making the Human-in-the-Loop feature robust and native to the workflow.
2. **HTML/JS vs Streamlit**: We replaced Streamlit with a vanilla HTML/JS frontend to allow for completely asynchronous, 1-second interval streaming of synthetic vitals without fighting Streamlit's re-render loop.
3. **Groq Model Selection**: Due to rapid model decommissioning on Groq's platform, the system is currently configured to use `qwen/qwen3.8-27b`, which was verified as actively supported and functioning for structured JSON output on the current API tier.
4. **Global 30-Second Refresh**: To keep the dashboard clean, `app.js` enforces a strict 30-second epoch where all active patient alert states and the alert board are reset, representing 30-minute block windows.
5. **Paused Graph Protection**: `api/server.py` explicitly checks if `human_in_loop` is in the `current_state.next` queue. If it is, it drops incoming vital stream updates to prevent LangGraph from auto-resuming and bypassing the clinician's decision.

---

## 6. Current Bugs or Issues

None known at this time. The end-to-end pipeline (Data Generation -> Backend API -> LangGraph -> RAG -> Groq LLM -> UI Rendering -> Clinician Decision -> Graph Resume) is fully operational.
