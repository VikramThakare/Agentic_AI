# PROJECT_CONTEXT.md — Handoff Document

**Project**: Agentic Clinical Deterioration & Escalation Copilot  
**Last Updated**: 2026-09-20  
**Disclaimer**: Educational prototype only. Not a medical device. Not for clinical use.

---

## 1. Project Overview & Objective

This is a prototype clinical decision-support system that monitors a simulated real-time stream of patient vital signs. It maintains per-patient state, detects multi-parameter deterioration trends, and escalates genuine persistent cases to a clinician with an **AI-generated, evidence-grounded recommendation** powered by the Groq API (using the Qwen 3.8 27B model).

The system avoids "alarm fatigue" by requiring deterioration to persist across 3 consecutive readings before alerting. A **ClinicalEscalationAgent** (LLM-powered, tool-using agent) investigates each triggered alert by retrieving patient context, vital history, and a relevant clinical protocol via TF-IDF RAG, then generates a structured recommendation for clinician review.

---

## 2. Current Project Status

**All core milestones are COMPLETE:**
- ✅ Synthetic data generation (6 patients, 60-minute vital stream)
- ✅ SQLite database schema and ingestion pipeline
- ✅ Patient state management
- ✅ Trend/deterioration detection engine (threshold-based, rolling window)
- ✅ Alert persistence (3-reading rule) and cooldown (10 min)
- ✅ TF-IDF RAG retrieval system (`retrieval.py`)
- ✅ Groq-powered `ClinicalEscalationAgent` with 3 tools (`agent.py`)
- ✅ Structured JSON output mapped to a Pydantic schema
- ✅ Graceful fallback when LLM is unavailable
- ✅ Streamlit dashboard with real-time charts
- ✅ Clinician-in-the-loop actions (Accept/Dismiss/Defer/Investigate)
- ✅ Audit trail logging
- ✅ Tests for tools and agent (`test_agent.py`, `test_m3.py`)

**The agent has been confirmed working end-to-end with a live Groq API call.** Rate limiting issues experienced previously on Gemini/xAI have been mitigated by switching to Groq's high-speed inference layer.

---

## 3. Folder/File Structure

```
AgeniAi/
├── .env                          # API key (GROQ_API_KEY) — DO NOT COMMIT
├── .env.example                  # Template for .env
├── README.md                     # Project overview and setup instructions
├── requirements.txt              # Python dependencies
├── copilot.db                    # SQLite database (auto-generated)
├── patients.csv                  # Synthetic patient demographics (auto-generated)
├── vitals_stream.csv             # 60-minute synthetic vital stream (auto-generated)
│
├── generate_synthetic_data.py    # Creates patients.csv and vitals_stream.csv
├── db_setup.py                   # Creates copilot.db with all table schemas
├── ingestion.py                  # Loads patients.csv into the database
│
├── trend.py                      # TrendEngine — rolling-window deterioration detection
├── alerts.py                     # AlertManager — persistence, cooldown, agent invocation
├── state.py                      # PatientStateManager — orchestrates the pipeline
├── retrieval.py                  # ProtocolRetriever — TF-IDF RAG system
├── agent.py                      # ClinicalEscalationAgent — Groq LLM agent with 3 tools
├── audit.py                      # AuditLogger — immutable event logging
├── app.py                        # Streamlit dashboard (main entry point)
│
├── test_m3.py                    # Tests for threshold/trend engine
├── test_agent.py                 # Tests for agent tools and fallback logic
│
├── config/
│   └── thresholds.yaml           # Vital sign threshold configuration
│
└── data/
    └── protocols/
        ├── respiratory.md        # Respiratory deterioration protocol
        └── cardiovascular.md     # Cardiovascular deterioration protocol
```

---

## 4. Purpose of Every Important File

| File | Purpose |
|------|---------|
| `generate_synthetic_data.py` | Creates 6 synthetic patients and a deterministic 60-minute vital stream. P-001 is stable, P-002 has noisy SpO2, P-003 has respiratory deterioration (min 20), P-004 has cardiovascular deterioration (min 15), P-005 deteriorates then recovers (min 10-30), P-006 has missing data (min 25). |
| `db_setup.py` | Creates `copilot.db` with 6 tables: `patients`, `vital_readings`, `patient_states`, `alerts`, `evidence_records`, `audit_events`. |
| `ingestion.py` | Loads `patients.csv` into the `patients` table. Called once during setup. |
| `trend.py` | `TrendEngine` class. Loads `config/thresholds.yaml`. Evaluates the latest vital reading against patient baselines using a rolling window. Returns `deteriorating` status with a point score and list of concerning signals if ≥2 vitals breach thresholds simultaneously. |
| `alerts.py` | `AlertManager` class. Calls `TrendEngine` 3 times to check if deterioration persists across 3 consecutive readings. Enforces a 10-minute cooldown between alerts for the same patient. On alert trigger, invokes the `ClinicalEscalationAgent`, formats the structured response into markdown, saves to the `alerts` table, logs to `evidence_records` and `audit_events`. |
| `state.py` | `PatientStateManager` class. Orchestrates the per-patient pipeline: inserts vital reading → evaluates trend → calls `AlertManager.process_trend()` → updates `patient_states` table with risk score and active alert ID. |
| `retrieval.py` | `ProtocolRetriever` class. Loads all `.md` files from `data/protocols/`. Builds a TF-IDF matrix using scikit-learn. `find_protocol(query)` computes cosine similarity against the query and returns the best-matching protocol document with its full text. |
| `agent.py` | `ClinicalEscalationAgent` class. Uses the official OpenAI SDK pointing to Groq's API endpoint. Defines 3 tools: `get_patient_context()`, `get_vital_history()`, `get_clinical_protocol()`. Gathers evidence synchronously, makes a single API call to Groq, and returns a structured JSON response verified via Pydantic schema (`RecommendationOutput`). Falls back gracefully to a static response if the API key is missing or the LLM fails. |
| `audit.py` | `AuditLogger` class. `log_event()` writes to the `audit_events` table. `record_clinician_action()` updates the alert status and logs the clinician's decision. |
| `app.py` | Streamlit dashboard. Displays a Cohort Overview table, per-patient vital trend charts, and an Active Alert Queue with clinician action buttons (Accept/Dismiss/Defer/Investigate). Uses `st.session_state` for the simulated time pointer and supports Play/Pause/Step controls. |
| `config/thresholds.yaml` | Defines normal ranges and severity tiers for HR, SpO2, RR, Systolic BP, and Diastolic BP. |
| `data/protocols/respiratory.md` | Clinical protocol for respiratory deterioration (SpO2 drop + RR increase). |
| `data/protocols/cardiovascular.md` | Clinical protocol for cardiovascular deterioration (HR changes + BP changes). |
| `test_m3.py` | Tests for the `TrendEngine` threshold logic. |
| `test_agent.py` | Tests the 3 agent tools independently and tests the agent's fallback behavior. |

---

## 5. Technologies, Libraries, APIs, Models, and Tools

| Category | Technology |
|----------|------------|
| Language | Python 3.12 |
| Database | SQLite (single file: `copilot.db`) |
| Dashboard | Streamlit 1.31.0 |
| Charts | Plotly 5.18.0 |
| Data | Pandas 2.2.0, NumPy 1.26.4 |
| ML/Retrieval | scikit-learn 1.4.0 (TF-IDF + cosine similarity) |
| LLM SDK | `openai` (Official OpenAI SDK acting as client) |
| LLM Model | Groq API (`qwen/qwen3.8-27b`) |
| Schema | Pydantic 2.13.5 (structured output validation) |
| Config | PyYAML 6.0.1 |
| Environment | python-dotenv 1.2.3 |
| Testing | pytest 8.0.0 |

---

## 6. Database Schema (`copilot.db`)

### `patients`
| Column | Type | Description |
|--------|------|-------------|
| patient_id | TEXT PK | e.g., "P-001" |
| age | INTEGER | Patient age |
| history | TEXT | JSON array of medical history |
| medications | TEXT | JSON array of current medications |
| recent_labs | TEXT | JSON object of lab values |
| baseline | TEXT | JSON object of baseline vital signs |

### `vital_readings`
| Column | Type | Description |
|--------|------|-------------|
| reading_id | INTEGER PK | Auto-increment |
| patient_id | TEXT FK | References patients |
| timestamp | TEXT | ISO format timestamp |
| heart_rate_bpm | REAL | Heart rate |
| spo2_percent | REAL | Oxygen saturation |
| respiratory_rate_bpm | REAL | Respiratory rate |
| systolic_bp_mmhg | REAL | Systolic blood pressure |
| diastolic_bp_mmhg | REAL | Diastolic blood pressure |
| source | TEXT | e.g., "monitor" |
| validation_status | TEXT | Unused currently |

### `patient_states`
| Column | Type | Description |
|--------|------|-------------|
| patient_id | TEXT PK | References patients |
| last_reading_id | INTEGER | Latest reading ID |
| trend_summary | TEXT | JSON trend data |
| risk_score | REAL | Computed risk score |
| risk_category | TEXT | "low", "high", "critical" |
| active_alert_id | TEXT | Current active alert ID or None |
| updated_at | TEXT | Last update timestamp |

### `alerts`
| Column | Type | Description |
|--------|------|-------------|
| alert_id | TEXT PK | e.g., "AL-e4fb805b" |
| patient_id | TEXT FK | References patients |
| created_at | TEXT | Alert creation timestamp |
| status | TEXT | "active", "dismissed", "accepted", "deferred", "investigated" |
| priority_score | REAL | Computed priority score |
| trigger_summary | TEXT | JSON with signals, reason, and full agent structured response |
| recommendation_text | TEXT | Formatted markdown recommendation for dashboard display |
| cooldown_until | TEXT | Timestamp until next alert is suppressed |

### `evidence_records`
| Column | Type | Description |
|--------|------|-------------|
| record_id | INTEGER PK | Auto-increment |
| alert_id | TEXT FK | References alerts |
| patient_id | TEXT FK | References patients |
| document_id | TEXT | Protocol filename (e.g., "respiratory.md") |
| section_title | TEXT | Protocol section |
| text_excerpt | TEXT | Full JSON structured response from agent |
| retrieval_timestamp | TEXT | When the retrieval occurred |

### `audit_events`
| Column | Type | Description |
|--------|------|-------------|
| event_id | INTEGER PK | Auto-increment |
| alert_id | TEXT | Related alert ID |
| patient_id | TEXT | Related patient ID |
| event_type | TEXT | "ALERT_GENERATED", "CLINICIAN_ACTION" |
| event_data | TEXT | JSON payload with details |
| timestamp | TEXT | Event timestamp |

---

## 7. Features Already Implemented

1. Synthetic patient and vital data generation (6 patients, 60 min)
2. SQLite database with 6 tables
3. Data ingestion pipeline
4. Per-patient state tracking
5. Rolling-window trend detection with configurable YAML thresholds
6. Multi-signal deterioration detection (≥2 vital channels)
7. Alert persistence rule (3 consecutive deteriorating readings required)
8. Alert cooldown (10-minute suppression after an alert)
9. TF-IDF RAG protocol retrieval from `data/protocols/`
10. LLM-powered `ClinicalEscalationAgent` with 3 tools (via Groq API)
11. Structured output via Groq JSON mode and Pydantic validation
12. Graceful fallback when Groq API is unavailable
13. Streamlit real-time dashboard with Play/Pause/Step
14. Per-patient vital trend charts (Plotly)
15. Clinician action buttons (Accept/Dismiss/Defer/Investigate)
16. Audit trail logging for alert generation and clinician actions
17. Tests for threshold engine and agent tools

---

## 8. Features Partially Implemented

None. All planned features are complete.

---

## 9. Features Still Remaining

No features are explicitly remaining from the original requirements. Potential enhancements:
- More clinical protocols in `data/protocols/` for broader coverage
- Adding more comprehensive pytest-based tests
- Adding a `.gitignore` to exclude `.env` and `copilot.db`

---

## 10. Important Technical Decisions

1. **Dropped ML models in favor of LLM + AI Agents**: Originally considered Random Forest / ML for deterioration detection, but decided that threshold-based detection + LLM reasoning was more appropriate for the use case.
2. **Switched to Groq (via OpenAI SDK)**: Replaced Google Antigravity/Gemini to bypass the strict free-tier quota (20 requests/day). Groq provides incredibly fast inference and generous rate limits for agentic workflows.
3. **Synchronous Tool Calling**: The agent gathers evidence from tools locally and synchronously *before* sending a single prompt to the LLM, reducing API roundtrips from 3-4 down to just 1 per alert.
4. **Kept TF-IDF for RAG** instead of adding a vector database (FAISS/Chroma). The protocol knowledge base is small enough that TF-IDF + cosine similarity works well.
5. **Signal cleaning** in `get_clinical_protocol()`: Snake-case signal names (e.g., `spo2_percent`) are cleaned to natural language (`spo2 percent`) before TF-IDF matching.
6. **Explicit `.env` path**: `load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)` is used because relative `load_dotenv()` can fail depending on the working directory.

---

## 11. Important Bugs/Errors Encountered and Solutions

| Bug | Root Cause | Solution |
|-----|-----------|----------|
| API 429 Quota Exceeded (Gemini) | Gemini Free Tier is limited to 20 requests per day | Switched backend to Groq for high limits and faster inference |
| `model_not_found` / `model_decommissioned` | Groq frequently rotates model string names | Queried API directly, switched to `qwen/qwen3.8-27b` which works reliably |
| TF-IDF returning no match | Snake-case signals (`spo2_percent`) didn't match protocol text | Added signal cleaning: `replace("_", " ").replace("bpm", "")` |
| Streamlit `protobuf` conflict | Older packages installing `protobuf 7.x`, Streamlit needs `<6` | Known pip warning; does not crash the app |

---

## 12. Current Bugs or Issues

1. **Protobuf version conflict**: Some packages may attempt to require `protobuf>=7`, but `streamlit 1.31.0` works best with `<6`. This produces a pip warning but the app runs without crashing.

---

## 13. Important Commands

```bash
# Install all dependencies
pip install -r requirements.txt

# Generate synthetic data
python generate_synthetic_data.py

# Initialize database
python db_setup.py

# Load patients into database
python ingestion.py

# Run the Streamlit dashboard
streamlit run app.py

# Test agent tools and fallback
python test_agent.py

# Test threshold engine
python -m pytest test_m3.py -v
```

---

## 14. Environment Variables and Configuration

| Variable | Source | Required |
|----------|--------|----------|
| `GROQ_API_KEY` | `.env` file | Yes (for live agent; fallback works without it) |

Get a key from: https://console.groq.com/keys

The `.env` file must be in the project root directory (same folder as `agent.py`).

---

## 15. Current Architecture and Data Flow

```
Synthetic Vital Stream (vitals_stream.csv)
         ↓
     app.py reads one row per simulated minute
         ↓
     state.py → PatientStateManager.update()
         ↓
     Inserts vital into vital_readings table
         ↓
     trend.py → TrendEngine.evaluate()
         ↓
     Checks ≥2 vitals breaching thresholds simultaneously
         ↓
     alerts.py → AlertManager.process_trend()
         ↓
     Persistence check (3 consecutive deteriorating readings)
         ↓
     Cooldown check (10-minute suppression)
         ↓
     agent.py → ClinicalEscalationAgent.generate_recommendation()
         │
         ├── get_patient_context(patient_id)   → SQLite query
         ├── get_vital_history(patient_id)     → SQLite query
         └── get_clinical_protocol(signals)    → TF-IDF RAG
                        │
                        ↓
                 Retrieved Evidence Context
                        │
                        ↓
                 Groq API (Qwen 3.8 27B)
                        │
                        ↓
            Structured JSON (RecommendationOutput)
                        ↓
                 alerts table (recommendation_text)
                 evidence_records table
                 audit_events table
                        ↓
             Streamlit Dashboard (app.py)
                        ↓
                 Clinician Reviews Alert
                        ↓
            Accept / Dismiss / Defer / Investigate
                        ↓
                   audit_events table
```

---

## 16. Important Assumptions and Constraints

1. This is an **educational prototype** — not for clinical use.
2. The system uses **synthetic data only** — no real patient data.
3. Deterioration detection is **threshold-based** (not ML-based).
4. The LLM is used **only for recommendation generation**, not for deterioration detection.
5. The clinician **always makes the final decision** — the AI never acts autonomously.
6. The system uses a **single SQLite file** — no external databases.
7. The agent gathers evidence synchronously locally via tools and makes **exactly 1 API call per alert** to maximize performance and minimize rate limit impact.

---

## 17. Exact Next Steps for Continuing Development

1. **Add `.gitignore`**: Exclude `.env`, `copilot.db`, `__pycache__/`, `*.csv` from version control.
2. **Add more protocols**: Create additional `.md` files in `data/protocols/` for sepsis, neurological, and other deterioration patterns to broaden RAG coverage.
3. **Upgrade Streamlit**: Update to a version compatible with `protobuf>=7` to resolve the dependency warning.
4. **Add comprehensive tests**: Expand `test_agent.py` with pytest fixtures that mock the OpenAI/Groq API for reliable CI/CD testing without needing a real API key.

---

## 18. Additional Context

- The project was built iteratively over a single session. Milestones 1-4 (data generation, DB, trend engine, dashboard) were completed first, followed by the Agentic AI layer.
- The `ClinicalEscalationAgent` was confirmed working with a live Groq API call that returned a clinically grounded recommendation for patient P-003 (71yo, COPD), referencing the `respiratory.md` protocol.
- The `.env.example` file in the repo contains a placeholder key. The actual `.env` file (not committed) contains the working key.
- When demonstrating the system, expect alerts for P-004 around simulated minute 18 and P-003 around simulated minute 23.
