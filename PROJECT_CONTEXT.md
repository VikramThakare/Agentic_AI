# PROJECT_CONTEXT.md — Handoff Document & Implementation Details

**Project**: Agentic Clinical Deterioration & Escalation Copilot (LangGraph Architecture)
**Last Updated**: 2026-09-27
**Disclaimer**: Educational prototype only. Not a medical device. Not for clinical use.

---

## 1. Project Objective & Vision

This system is an agent-driven clinical decision-support prototype. It monitors continuous streams of patient vital signs to track evolving physiological states. The primary objective is to detect persistent, multi-parameter deterioration trends (such as early signs of sepsis, respiratory failure, or cardiac events) and intelligently escalate them.

To ensure clinical safety and reduce alert fatigue:
1. **Persistence Checks**: A single abnormal reading is ignored; trends must persist across multiple rolling window ticks.
2. **Evidence-Grounded AI**: Escalations are powered by RAG (retrieving exact clinical protocols) and structured LLM generation (via OpenRouter) to provide clinicians with clear, justifiable recommendations.
3. **Strict Human-in-the-Loop (HITL)**: Once an escalation is generated, the agentic loop is forcibly paused. No further automated actions are taken for that patient until a human clinician explicitly reviews and resolves the alert.

---

## 2. Technical Stack & Architecture

- **Backend Framework**: FastAPI (Python)
- **Agent Orchestration**: LangGraph (`StateGraph`, `MemorySaver`)
- **LLM Provider**: OpenRouter API (`openrouter/free` model) via LangChain
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (No build process required)
- **State Schema**: Strictly typed via `TypedDict` and `Pydantic`

### LangGraph Workflow Details
The state machine for each patient is defined in `graph/workflow.py` and maintains a dedicated `thread_id` corresponding to the `patient_id`. 

**The Node Sequence:**
1. `ingest_reading`: Maintains a rolling buffer of the last 30 readings.
2. `update_profile`: Injects static patient history and demographics from the local CSV.
3. `detect_trend`: A rule-based engine evaluating the buffer against thresholds (e.g., SpO2 < 92 & RR > 22 for respiratory distress).
4. `retrieve_evidence` (Conditional): If a trend is detected, this node performs a TF-IDF search against local clinical protocols.
5. `reason_generate` (Conditional): Calls the OpenRouter LLM, injecting the patient history, recent vitals, and retrieved protocol to generate a structured `ClinicalRecommendation`.
6. `human_in_loop`: The graph execution is interrupted *before* this node. It awaits external API input.
7. `audit_log_write`: Logs the final clinician decision and closes the cycle.

---

## 3. Directory Structure

```text
AgeniAi/
├── .env                          # Environment variables (OPENROUTER_API_KEY)
├── README.md                     # High-level overview and setup guide
├── PROJECT_CONTEXT.md            # Detailed architecture and implementation plans
├── requirements.txt              # Python dependency list
│
├── api/
│   └── server.py                 # FastAPI server; compiles LangGraph & exposes endpoints
│
├── frontend/
│   ├── index.html                # Real-time dashboard layout
│   ├── app.js                    # Synthetic stream generator, UI logic, and API calls
│   └── styles.css                # Dashboard styling and layout rules
│
├── graph/
│   ├── workflow.py               # Defines the LangGraph StateGraph edges and conditional routing
│   └── nodes.py                  # Contains the execution logic for every LangGraph node
│
├── state/
│   └── schema.py                 # Defines the PatientState and Alert structures
│
├── data/
│   └── protocols/                # Clinical markdown files used as the corpus for RAG
│
├── db_setup.py                   # Script for initializing local DB/schema (if applicable)
├── generate_synthetic_data.py    # Script to regenerate the synthetic vital stream dataset
├── patients.csv                  # Mock local database of patient demographics and history
└── vitals_stream.csv             # Generated mock data stream read by the frontend simulator
```
*(Note: Legacy files like `ingestion.py` and `scratch_models.py` have been safely removed to reduce technical debt).*

---

## 4. Key Design Decisions

1. **LangGraph over Static Loops**: Transitioning to LangGraph provided native support for checkpointers. This made implementing the `interrupt_before=["human_in_loop"]` feature highly reliable, ensuring the system safely suspends state without complex external caching.
2. **Vanilla Frontend**: Bypassing heavy frameworks (React/Next) or Python UI tools (Streamlit) allowed the frontend to execute an infinite, non-blocking `setInterval` loop to simulate 1-second vital stream ticks smoothly.
3. **OpenRouter API**: The system utilizes OpenRouter (defaulting to the `openrouter/free` model) for LLM reasoning to ensure reliable structured JSON output via Pydantic parsers, avoiding rate-limit bottlenecks experienced with other free-tier providers.
4. **Dynamic Data Generation**: Patient CRUD operations via the API dynamically execute `generate_synthetic_data.py` in the background, instantly rebuilding the `vitals_stream.csv` feed to reflect new or updated patients seamlessly.
5. **Epoch Reset**: The frontend dashboard automatically clears old alerts globally every 30 seconds to simulate shifts and keep the dashboard clean.

---

## 5. Current Status

**All core components are complete and operational.** The end-to-end pipeline successfully routes streaming data, triggers LangGraph state transitions, performs RAG retrieval, outputs structured LLM recommendations, and respects the clinician pause mechanism.
