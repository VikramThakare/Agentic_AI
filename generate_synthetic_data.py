import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta

def generate_vitals_stream(seed=42, minutes=60):
    np.random.seed(seed)
    start_time = datetime(2026, 1, 1, 8, 0, 0)
    
    if not os.path.exists("patients.csv"):
        print("patients.csv not found!")
        return pd.DataFrame()
        
    patients_df = pd.read_csv("patients.csv")
    
    records = []
    for t in range(minutes):
        current_time = start_time + timedelta(minutes=t)
        
        for _, patient in patients_df.iterrows():
            pid = patient["patient_id"]
            
            # Default logic for generic patients
            hr = int(np.random.normal(70, 2))
            spo2 = int(np.clip(np.random.normal(98, 1), 0, 100))
            rr = int(np.random.normal(14, 1))
            sys_bp = int(np.random.normal(120, 3))
            dia_bp = int(np.random.normal(80, 2))
            
            if pid == "P-002":
                hr = int(np.random.normal(75, 2))
                spo2 = 97
                if t % 15 == 0 and t > 0:
                    spo2 = 85
                rr = int(np.random.normal(16, 1))
                sys_bp = int(np.random.normal(130, 3))
                dia_bp = int(np.random.normal(85, 2))
            elif pid == "P-003":
                hr = int(np.random.normal(85, 2))
                spo2 = 94
                rr = 18
                if t >= 20:
                    spo2 -= int((t - 20) * 0.3)
                    rr += int((t - 20) * 0.4)
                    spo2 = max(80, spo2)
                    rr = min(35, rr)
                sys_bp = int(np.random.normal(135, 3))
                dia_bp = int(np.random.normal(85, 2))
            elif pid == "P-004":
                hr = 65
                sys_bp = 115
                dia_bp = 75
                if t >= 15:
                    hr += int((t - 15) * 1.5)
                    sys_bp -= int((t - 15) * 1.5)
                    dia_bp -= int((t - 15) * 0.8)
                    hr = min(140, hr)
                    sys_bp = max(70, sys_bp)
                    dia_bp = max(40, dia_bp)
            elif pid == "P-005":
                hr = 80
                spo2 = 97
                if 10 <= t < 30:
                    hr += int((t - 10) * 1.2)
                    spo2 -= int((t - 10) * 0.5)
                elif t >= 30:
                    hr = 80 + max(0, int(24 - (t - 30) * 2))
                    spo2 = 87 + min(10, int((t - 30) * 1))
            elif pid == "P-006":
                hr = int(np.random.normal(72, 2))
                spo2 = int(np.clip(np.random.normal(96, 1), 0, 100))
                if t >= 25:
                    spo2 = np.nan
            
            records.append({
                "patient_id": pid,
                "timestamp": current_time,
                "heart_rate_bpm": hr,
                "spo2_percent": spo2,
                "respiratory_rate_bpm": rr,
                "systolic_bp_mmhg": sys_bp,
                "diastolic_bp_mmhg": dia_bp,
                "source": "monitor"
            })
            
    return pd.DataFrame(records)

if __name__ == "__main__":
    print("Generating synthetic data based on patients.csv...")
    vitals_df = generate_vitals_stream()
    vitals_df.to_csv("vitals_stream.csv", index=False)
    print("Generated vitals_stream.csv successfully.")
