import sqlite3
import os

DB_NAME = "copilot.db"

def init_db():
    if os.path.exists(DB_NAME):
        print(f"Database {DB_NAME} already exists. Recreating it.")
        os.remove(DB_NAME)
        
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create patients table
    cursor.execute("""
    CREATE TABLE patients (
        patient_id TEXT PRIMARY KEY,
        age INTEGER,
        history TEXT,
        medications TEXT,
        recent_labs TEXT,
        baseline TEXT
    )
    """)
    
    # Create vital_readings table
    cursor.execute("""
    CREATE TABLE vital_readings (
        reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        timestamp TEXT,
        heart_rate_bpm REAL,
        spo2_percent REAL,
        respiratory_rate_bpm REAL,
        systolic_bp_mmhg REAL,
        diastolic_bp_mmhg REAL,
        source TEXT,
        validation_status TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
    )
    """)
    
    # Create patient_states table
    cursor.execute("""
    CREATE TABLE patient_states (
        patient_id TEXT PRIMARY KEY,
        last_reading_id INTEGER,
        trend_summary TEXT,
        risk_score REAL,
        risk_category TEXT,
        active_alert_id TEXT,
        updated_at TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
    )
    """)
    
    # Create alerts table
    cursor.execute("""
    CREATE TABLE alerts (
        alert_id TEXT PRIMARY KEY,
        patient_id TEXT,
        created_at TEXT,
        status TEXT,
        priority_score REAL,
        trigger_summary TEXT,
        recommendation_text TEXT,
        cooldown_until TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
    )
    """)
    
    # Create evidence_records table
    cursor.execute("""
    CREATE TABLE evidence_records (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_id TEXT,
        patient_id TEXT,
        document_id TEXT,
        section_title TEXT,
        text_excerpt TEXT,
        retrieval_timestamp TEXT,
        FOREIGN KEY(alert_id) REFERENCES alerts(alert_id)
    )
    """)
    
    # Create audit_events table
    cursor.execute("""
    CREATE TABLE audit_events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_id TEXT,
        patient_id TEXT,
        event_type TEXT,
        event_data TEXT,
        timestamp TEXT
    )
    """)
    
    conn.commit()
    conn.close()
    print(f"Database {DB_NAME} initialized successfully with all schemas.")

if __name__ == "__main__":
    init_db()
