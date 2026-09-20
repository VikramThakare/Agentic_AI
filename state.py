import sqlite3
import pandas as pd
from datetime import datetime
import json
from trend import TrendEngine
from alerts import AlertManager

DB_NAME = "copilot.db"

class PatientStateManager:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.trend_engine = TrendEngine()
        self.alert_manager = AlertManager(self.conn, self.trend_engine)

    def update_state(self, reading_id, patient_id):
        """Updates the patient state based on the latest reading."""
        cursor = self.conn.cursor()
        
        # 1. Fetch the reading
        cursor.execute("SELECT * FROM vital_readings WHERE reading_id = ?", (reading_id,))
        reading = cursor.fetchone()
        
        if not reading:
            print(f"Reading {reading_id} not found.")
            return
            
        now = datetime.now().isoformat()
        
        # 2. Get patient history (last 5 readings for trend window)
        history_df = self.get_patient_history(patient_id, limit=5)
        
        # 3. Evaluate Trend & Alerts
        alert_result = self.alert_manager.process_trend(patient_id, history_df)
        
        # 4. Update patient state with the latest reading ID, timestamp, and alert info
        if alert_result:
            cursor.execute("""
                UPDATE patient_states 
                SET last_reading_id = ?, updated_at = ?, risk_score = ?, risk_category = ?, active_alert_id = ?
                WHERE patient_id = ?
            """, (
                reading_id, now, 
                alert_result['priority_score'], 
                alert_result['risk_category'], 
                alert_result['alert_id'], 
                patient_id
            ))
        else:
            # Evaluate single point trend summary just for state keeping
            trend_res = self.trend_engine.evaluate(history_df)
            cursor.execute("""
                UPDATE patient_states 
                SET last_reading_id = ?, updated_at = ?, trend_summary = ?
                WHERE patient_id = ?
            """, (reading_id, now, json.dumps(trend_res), patient_id))
        
        self.conn.commit()
        
    def get_patient_history(self, patient_id, limit=10):
        """Fetches the recent history for a patient."""
        query = f"SELECT * FROM vital_readings WHERE patient_id = '{patient_id}' ORDER BY timestamp DESC LIMIT {limit}"
        df = pd.read_sql_query(query, self.conn)
        return df.sort_values('timestamp')

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    state_manager = PatientStateManager()
    print("PatientStateManager initialized.")
    state_manager.close()
