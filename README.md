# Agentic Clinical Deterioration & Escalation Copilot

**Disclaimer: Educational prototype only. Not a medical device. Not for clinical use or diagnosis.**

## Overview

This project is a prototype clinical decision-support system designed to monitor a simulated real-time stream of patient vital signs. It maintains an evolving per-patient state and intelligently detects multi-parameter deterioration trends to escalate cases to a clinician with a clear, evidence-grounded explanation.

This avoids "alarm fatigue" caused by naive single-threshold alerts, ensuring only genuine, persistent multi-signal deteriorations are flagged.

## Architecture & Agent Loop

The system relies on a clean, single-app architecture using Python and SQLite:

1. **Synthetic Stream Generator** (`generate_synthetic_data.py`): Creates simulated patients and a deterministic 60-minute stream of vitals.
2. **Ingestion & State Manager** (`ingestion.py`, `state.py`): Ingests the stream and updates the `patient_states` memory.
3. **Trend & Risk Engine** (`trend.py`): Evaluates rolling windows of vital history to detect if >= 2 vital channels are moving in a concerning direction based on configured thresholds.
4. **Alert Manager** (`alerts.py`): Applies a persistence rule (deterioration must span >= 3 consecutive readings) and a cooldown period (5-10 minutes) before logging an active alert to the database.

## Setup & Execution

### Requirements
- Python 3.11+
- Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. **Generate Synthetic Data**:
```bash
python generate_synthetic_data.py
```
*(This produces `patients.csv` and `vitals_stream.csv`)*

2. **Initialize Database**:
```bash
python db_setup.py
```
*(This creates `copilot.db` and the required schemas)*

3. **Run Data Ingestion**:
```bash
python ingestion.py
```
*(This loads the patient contexts into the database)*

*Note: The full Streamlit dashboard and real-time processing loop will be integrated in Milestone 4.*
