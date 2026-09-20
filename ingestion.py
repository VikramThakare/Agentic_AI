import sqlite3
import pandas as pd
from datetime import datetime
import json

DB_NAME = "copilot.db"

class DataIngestor:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        
    def load_patients(self, patients_csv="patients.csv"):
        """Loads patients from CSV into the database if not already present."""
        df = pd.read_csv(patients_csv)
        cursor = self.conn.cursor()
        
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT OR IGNORE INTO patients (patient_id, age, history, medications, recent_labs, baseline)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                row['patient_id'],
                row['age'],
                row['history'],
                row['medications'],
                row['recent_labs'],
                row['baseline']
            ))
            
            # Initialize patient state if not exists
            cursor.execute("""
                INSERT OR IGNORE INTO patient_states (patient_id, last_reading_id, trend_summary, risk_score, risk_category, active_alert_id, updated_at)
                VALUES (?, NULL, '{}', 0.0, 'low', NULL, ?)
            """, (row['patient_id'], datetime.now().isoformat()))
            
        self.conn.commit()
        print(f"Loaded {len(df)} patients into the database.")

    def ingest_reading(self, reading_dict):
        """Ingests a single reading into the database."""
        cursor = self.conn.cursor()
        
        # Validation
        status = "valid"
        if pd.isna(reading_dict.get('spo2_percent')) or pd.isna(reading_dict.get('heart_rate_bpm')):
            status = "invalid" # Simple validation for missing data
        
        cursor.execute("""
            INSERT INTO vital_readings (
                patient_id, timestamp, heart_rate_bpm, spo2_percent,
                respiratory_rate_bpm, systolic_bp_mmhg, diastolic_bp_mmhg,
                source, validation_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            reading_dict['patient_id'],
            reading_dict['timestamp'],
            reading_dict['heart_rate_bpm'] if not pd.isna(reading_dict['heart_rate_bpm']) else None,
            reading_dict['spo2_percent'] if not pd.isna(reading_dict['spo2_percent']) else None,
            reading_dict['respiratory_rate_bpm'] if not pd.isna(reading_dict['respiratory_rate_bpm']) else None,
            reading_dict['systolic_bp_mmhg'] if not pd.isna(reading_dict['systolic_bp_mmhg']) else None,
            reading_dict['diastolic_bp_mmhg'] if not pd.isna(reading_dict['diastolic_bp_mmhg']) else None,
            reading_dict.get('source', 'monitor'),
            status
        ))
        
        reading_id = cursor.lastrowid
        self.conn.commit()
        return reading_id

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    ingestor = DataIngestor()
    ingestor.load_patients()
    ingestor.close()
