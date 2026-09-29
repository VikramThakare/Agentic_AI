import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta

def generate_vitals_stream(seed=42, minutes=300):
    np.random.seed(seed)
    start_time = datetime(2026, 1, 1, 8, 0, 0)
    
    if not os.path.exists("patients.csv"):
        print("patients.csv not found!")
        return pd.DataFrame()
        
    patients_df = pd.read_csv("patients.csv")
    
    records = []
    
    # Initialize baseline state for each patient
    patient_states = {}
    
    # Track the number of patients to guarantee first two crash
    patient_index = 0
    
    for _, patient in patients_df.iterrows():
        pid = patient["patient_id"]
        
        # Randomly assign a crash to patients so any patient can become critical
        crash_type = np.random.choice(["resp", "cardio", "none"], p=[0.4, 0.4, 0.2])
        if crash_type != "none":
            crash_target = crash_type
            crash_start_time = np.random.randint(2, 6) # Crash starts between minute 2 and 5
        else:
            crash_target = "none"
            crash_start_time = 999
            
        patient_states[pid] = {
            "hr": np.random.normal(70, 5),
            "spo2": np.random.normal(98, 1),
            "rr": np.random.normal(14, 1),
            "sys_bp": np.random.normal(120, 5),
            "dia_bp": np.random.normal(80, 5),
            "crash_target": crash_target,
            "crash_start_time": crash_start_time
        }

    for t in range(minutes):
        current_time = start_time + timedelta(minutes=t)
        
        for _, patient in patients_df.iterrows():
            pid = patient["patient_id"]
            state = patient_states[pid]
            
            # Normal random walk (drift)
            state["hr"] += np.random.normal(0, 0.5)
            state["spo2"] += np.random.normal(0, 0.1)
            state["rr"] += np.random.normal(0, 0.1)
            state["sys_bp"] += np.random.normal(0, 0.5)
            state["dia_bp"] += np.random.normal(0, 0.2)
            
            if t < state["crash_start_time"]:
                # Bound normal vitals to prevent wild drifting before a crash
                state["hr"] = np.clip(state["hr"], 60, 100)
                state["spo2"] = np.clip(state["spo2"], 94, 100)
                state["rr"] = np.clip(state["rr"], 12, 18)
                state["sys_bp"] = np.clip(state["sys_bp"], 110, 140)
                state["dia_bp"] = np.clip(state["dia_bp"], 70, 90)
            else:
                # Introduce crash if past crash start time - increased severity!
                if state["crash_target"] == "resp":
                    # SpO2 drops severely, RR increases severely
                    state["spo2"] -= np.random.normal(1.0, 0.2)
                    state["rr"] += np.random.normal(0.8, 0.2)
                    state["spo2"] = np.clip(state["spo2"], 50, 100) # Allow it to drop very low
                    state["rr"] = np.clip(state["rr"], 12, 45)      # Allow it to rise very high
                elif state["crash_target"] == "cardio":
                    # HR spikes severely, BP drops severely
                    state["hr"] += np.random.normal(2.5, 0.5)
                    state["sys_bp"] -= np.random.normal(2.0, 0.5)
                    state["hr"] = np.clip(state["hr"], 60, 200)
                    state["sys_bp"] = np.clip(state["sys_bp"], 40, 140)
            
            records.append({
                "patient_id": pid,
                "timestamp": current_time,
                "heart_rate_bpm": int(state["hr"]),
                "spo2_percent": int(state["spo2"]),
                "respiratory_rate_bpm": int(state["rr"]),
                "systolic_bp_mmhg": int(state["sys_bp"]),
                "diastolic_bp_mmhg": int(state["dia_bp"]),
                "source": "monitor"
            })
            
    return pd.DataFrame(records)

if __name__ == "__main__":
    print("Generating synthetic data based on patients.csv...")
    vitals_df = generate_vitals_stream()
    vitals_df.to_csv("vitals_stream.csv", index=False)
    print("Generated vitals_stream.csv successfully.")
