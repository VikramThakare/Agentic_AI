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
        
        # Guarantee crashes for the first two patients, others are safe
        if patient_index == 0:
            crash_target = "resp"
            crash_start_time = 2  # Crash starts very early (at 2nd minute)
        elif patient_index == 1:
            crash_target = "cardio"
            crash_start_time = 3  # Crash starts very early (at 3rd minute)
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
        patient_index += 1

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
            
            # Bound normal vitals to prevent wild drifting before a crash
            state["hr"] = np.clip(state["hr"], 60, 100)
            state["spo2"] = np.clip(state["spo2"], 94, 100)
            state["rr"] = np.clip(state["rr"], 12, 18)
            state["sys_bp"] = np.clip(state["sys_bp"], 110, 140)
            state["dia_bp"] = np.clip(state["dia_bp"], 70, 90)
            
            # Introduce crash if past crash start time
            if t >= state["crash_start_time"]:
                if state["crash_target"] == "resp":
                    # SpO2 drops below 90, RR increases above 22
                    state["spo2"] -= np.random.normal(0.5, 0.2)
                    state["rr"] += np.random.normal(0.4, 0.2)
                    state["spo2"] = np.clip(state["spo2"], 70, 100) # Allow it to drop
                    state["rr"] = np.clip(state["rr"], 12, 35)      # Allow it to rise
                elif state["crash_target"] == "cardio":
                    # HR spikes above 120, BP drops below 90
                    state["hr"] += np.random.normal(1.5, 0.5)
                    state["sys_bp"] -= np.random.normal(1.2, 0.5)
                    state["hr"] = np.clip(state["hr"], 60, 160)
                    state["sys_bp"] = np.clip(state["sys_bp"], 50, 140)
            
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
