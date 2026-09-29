# Agentic Clinical Deterioration & Escalation Copilot

**Team ID: 36**

**Disclaimer**: This project is an educational prototype. It is **not** a medical device, nor is it intended for clinical use, diagnosis, or treatment.

---

## 📖 Overview

The Agentic Clinical Copilot is an advanced decision-support prototype designed to monitor a simulated, continuous stream of patient vital signs. Leveraging **LangGraph** for robust state management and **OpenRouter** for AI-driven clinical reasoning, the system intelligently detects multi-parameter physiological deterioration (e.g., compounding respiratory or cardiovascular distress) and escalates actionable, evidence-based recommendations to human clinicians.

To prevent "alarm fatigue," the agent enforces a strict multi-tick persistence threshold before escalating. When a genuine deterioration is detected, the workflow suspends itself—enforcing a **Human-in-the-Loop (HITL)** pause—and waits for a clinician to review the generated evidence and submit a decision before resuming the monitoring loop.

---

## 🏗️ Architecture

The system is built on a modern, decoupled real-time architecture:

1. **Frontend Dashboard (`frontend/`)**:
   - A lightweight, vanilla HTML/CSS/JS web application.
   - Generates and streams synthetic real-time patient vitals.
   - Features a dynamic UI for Patient CRUD operations, real-time vital charts, and an AI Escalation review panel.
2. **FastAPI Backend (`api/server.py`)**:
   - An asynchronous RESTful API serving as the system's entry point.
   - Ingests vital streams and acts as the LangGraph orchestrator.
3. **LangGraph Workflow (`graph/`)**:
   - Uses a `StateGraph` with a memory checkpointer.
   - Nodes include: `ingest_reading`, `update_profile`, `detect_trend`, `retrieve_evidence`, `reason_generate`, `human_in_loop`, and `audit_log_write`.
   - **RAG Integration**: Pulls clinical protocols via TF-IDF to ground LLM reasoning.
   - **LLM Reasoning**: Utilizes the OpenRouter API to evaluate vitals against protocols and generate structured Pydantic responses.

---

## 🚀 Setup & Execution

### Prerequisites

- **Python**: Version 3.11 or higher.
- **API Key**: An active OpenRouter API key (`openrouter/free` model is used by default).

### 1. Installation

Clone the repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory (you can copy `.env.example` if it exists) and add your OpenRouter API key:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 3. Launch the Backend Server

Start the FastAPI server. By default, it will run on port 8000.

```bash
python -m api.server
```

### 4. Launch the Frontend Dashboard

The frontend requires no build steps (no npm, webpack, or Next.js required).
Simply launch a local HTTP server in the root directory, or open the HTML file directly:

```bash
# Optional: Serve the frontend locally
python -m http.server 8080 --directory frontend
```

Navigate to `http://localhost:8080` (or `http://127.0.0.1:8080`) in your web browser. Click the **Start Simulation** button on the dashboard to initiate the live data stream.

---

## 🛠️ Usage Flow

1. **Monitor**: Watch the dashboard as synthetic vitals populate the charts.
2. **Trigger**: Wait for a simulated patient's vitals to cross the configured deterioration thresholds persistently.
3. **Review**: The system will escalate an alert and pause. Click "Review" on the affected patient to see the AI's RAG-backed recommendation.
4. **Action**: Click "Refer" or "Dismiss" in the UI to submit your clinician decision. This un-pauses the LangGraph thread, logs the audit, and resumes monitoring.
