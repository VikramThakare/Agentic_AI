import pandas as pd
from ingestion import DataIngestor
from state import PatientStateManager
import sqlite3
import db_setup

def test_m3():
    # 1. Init DB and load patients
    db_setup.init_db()
    
    ingestor = DataIngestor()
    ingestor.load_patients()
    
    # 2. Load stream data
    stream_df = pd.read_csv("vitals_stream.csv")
    
    state_manager = PatientStateManager()
    
    # Process the stream for P-003 (Respiratory Deterioration starts min 20)
    print("Simulating stream for P-003...")
    p003_data = stream_df[stream_df['patient_id'] == 'P-003']
    
    for _, row in p003_data.iterrows():
        reading_dict = row.to_dict()
        reading_id = ingestor.ingest_reading(reading_dict)
        state_manager.update_state(reading_id, "P-003")
        
    # Check if alert was generated
    conn = sqlite3.connect("copilot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alerts WHERE patient_id = 'P-003'")
    alerts = cursor.fetchall()
    
    print(f"\nGenerated {len(alerts)} alerts for P-003.")
    for a in alerts:
        print(f"Alert ID: {a[0]}, Created At: {a[2]}, Status: {a[3]}, Score: {a[4]}, Cooldown Until: {a[7]}")
        
    ingestor.close()
    state_manager.close()
    conn.close()

if __name__ == "__main__":
    test_m3()
