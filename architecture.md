# System Architecture

This document outlines the architecture for the **Agentic Clinical Copilot**, detailing how the frontend, backend, and LangGraph components interact.

## High-Level Architecture Diagram

```mermaid
graph TD
    %% Frontend Components
    subgraph Frontend [Frontend Dashboard (Vanilla HTML/JS)]
        UI[User Interface & Charts]
        Sim[Synthetic Data Generator]
    end

    %% Backend Components
    subgraph Backend [FastAPI Backend]
        API_Stream[POST /vitals/stream]
        API_Decision[POST /alerts/{id}/decision]
        API_CRUD[Patient CRUD Endpoints]
    end

    %% LangGraph Orchestration
    subgraph Agent [LangGraph State Machine]
        State[(PatientState \n MemorySaver)]
        N1[ingest_reading]
        N2[update_profile]
        N3[detect_trend]
        N4[retrieve_evidence]
        N5[reason_generate]
        N6[human_in_loop]
        N7[audit_log_write]
    end

    %% Data Stores
    subgraph Storage [Local Data & Knowledge Base]
        CSV_Patients[(patients.csv)]
        CSV_Vitals[(vitals_stream.csv)]
        RAG_Corpus[(Protocols Markdown)]
    end

    %% External Services
    LLM((OpenRouter API \n LLM))

    %% Connections
    Sim -- Streams 1/sec --> API_Stream
    API_Stream -- Injects into Thread --> State
    State --> N1
    N1 --> N2
    N2 --> N3
    
    %% Conditional Logic
    N3 -- Trend Detected --> N4
    N3 -- No Trend --> N7
    
    N4 -- Queries --> RAG_Corpus
    N4 --> N5
    N5 -- Prompts --> LLM
    LLM -- Structured JSON --> N5
    N5 --> N6
    
    %% Human in the Loop pause
    N6 -. Paused (Awaits Clinician) .-> UI
    UI -- Clinician Decision --> API_Decision
    API_Decision -- Resumes Thread --> N6
    N6 --> N7
    
    %% Background Tasks
    API_CRUD -- Triggers Script --> CSV_Vitals
    CSV_Patients -. read by .- N2
```

## Component Details

### 1. Frontend Dashboard (`frontend/`)
- **Technology**: Vanilla HTML, CSS, JavaScript (No bundler/framework).
- **Responsibility**: 
  - Simulates a real-time monitor by iterating through `vitals_stream.csv` and pushing data to the backend at 1-second intervals.
  - Dynamically renders physiological charts (using Chart.js) and updates patient status badges.
  - Intercepts LangGraph `human_in_loop` pauses to render an "AI Escalation" card for clinician review.

### 2. FastAPI Backend (`api/server.py`)
- **Technology**: Python, FastAPI.
- **Responsibility**: 
  - Exposes REST endpoints for the frontend.
  - Serves as the host container for LangGraph execution.
  - Checks if a LangGraph thread is currently paused before blindly injecting new vitals, ensuring data integrity during clinical review.
  - Manages Patient CRUD, which dynamically regenerates the `vitals_stream.csv` simulation dataset on the fly.

### 3. LangGraph Orchestration (`graph/`)
- **Technology**: LangGraph, LangChain.
- **State Definition (`schema.py`)**: A strictly typed `PatientState` dictionary tracking the rolling vitals buffer, active alerts, retrieved evidence, LLM escalations, and audit logs.
- **Nodes & Edges (`workflow.py` & `nodes.py`)**:
  - **`ingest_reading`**: Manages the rolling buffer window (last 30 ticks).
  - **`update_profile`**: Fetches static medical history and demographics to contextualize the incoming vitals.
  - **`detect_trend`**: A deterministic rule engine. It evaluates the buffer to ensure physiological aberrations are *persistent* (not anomalous artifacts) before flagging an alert.
  - **`retrieve_evidence`**: A TF-IDF RAG implementation. If an alert is triggered, it searches local clinical protocols (e.g., Sepsis, Respiratory Failure) for evidence-based next steps.
  - **`reason_generate`**: Leverages **OpenRouter** (`openrouter/free`) to process the vitals, patient history, and retrieved protocols, outputting a strictly formatted Pydantic schema (`ClinicalRecommendation`).
  - **`human_in_loop`**: The crux of the safety architecture. LangGraph is configured to `interrupt_before=["human_in_loop"]`. Execution halts entirely until the `/alerts/{patient_id}/decision` endpoint is called by a human.
  - **`audit_log_write`**: Finalizes the cycle by appending the decision to the patient's record.

### 4. RAG & LLM Integration
- **RAG Pipeline**: Driven by local markdown files (`data/protocols/`). By pulling exact protocol text into the LLM prompt, we eliminate hallucination and enforce hospital-standard compliance.
- **Structured Output**: The LLM output is guaranteed to follow a predefined JSON structure mapping to our `ClinicalRecommendation` class, ensuring the frontend can reliably parse and render Risk Scores, Severity Tiers, and Recommended Interventions without regex hacking.
