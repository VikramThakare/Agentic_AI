# Agentic Clinical Deterioration & Escalation Copilot (LangGraph Edition)

**Disclaimer: Educational prototype only. Not a medical device. Not for clinical use or diagnosis.**

## Overview

This project is an advanced, agentic clinical decision-support system designed to monitor a simulated real-time stream of patient vital signs. It maintains an evolving per-patient state using **LangGraph** to intelligently detect multi-parameter deterioration trends and escalate cases to a clinician with a clear, evidence-grounded explanation generated via **RAG (Retrieval-Augmented Generation)** and the **OpenRouter API**.

This avoids "alarm fatigue" by ensuring only genuine, persistent deteriorations are flagged. When a critical threshold is breached, the LangGraph workflow actively retrieves relevant medical protocols and synthesizes a recommendation before explicitly **pausing** execution to await a human clinician's decision (Human-in-the-Loop). The system also features a dynamic patient roster where users can **Add, Edit (History/Meds), and Remove patients** on the fly, seamlessly rebuilding the synthetic stream dataset without dropping the live feed.

## Architecture & Agent Loop

The system has been completely upgraded to a modern, real-time architecture:

1. **Frontend Dashboard (`frontend/`)**: A vanilla HTML/CSS/JS dashboard that generates infinite real-time synthetic vital streams (simulating 1 minute per tick) and streams them to the backend API.
2. **FastAPI Backend (`api/server.py`)**: An asynchronous REST API that receives the streaming vitals and pushes them into the LangGraph state machine.
3. **LangGraph Workflow (`graph/workflow.py` & `nodes.py`)**: The core orchestration engine. The state flows through:
   - `ingest_reading` -> `update_profile` -> `detect_trend`
   - *If deteriorating*: -> `retrieve_evidence` (RAG) -> `reason_generate` (OpenRouter LLM)
   - *Human-in-the-Loop*: The graph pauses before `human_in_loop` until the clinician approves or dismisses the alert via the UI.
   - *Resolution*: -> `audit_log_write`

## Setup & Execution

### Requirements
- Python 3.11+
- Install dependencies:
```bash
pip install -r requirements.txt
```

### 1. Set up Environment
Copy `.env.example` to `.env` and add your OpenRouter API key:
```bash
# Get your OpenRouter API key from https://openrouter.ai/keys
OPENROUTER_API_KEY=your_api_key_here
```

### 2. Run the FastAPI Backend
Start the backend server on port 8000:
```bash
python -m api.server
```

### 3. Open the Dashboard
Simply open the `frontend/index.html` file in any modern web browser (no build step or web server required). Click **Start Simulation** to begin the real-time vital signs stream!
