import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

def generate_patients():
    patients = [
        {
            "patient_id": "P-001",
            "age": 45,
            "history": json.dumps(["No significant past medical history"]),
            "medications": json.dumps(["None"]),
            "recent_labs": json.dumps({"WBC": 7.5, "Hgb": 14.2}),
            "baseline": json.dumps({"HR": 70, "SpO2": 98, "RR": 14, "SysBP": 120, "DiaBP": 80})
        },
        {
            "patient_id": "P-002",
            "age": 62,
            "history": json.dumps(["Type 2 Diabetes"]),
            "medications": json.dumps(["Metformin"]),
            "recent_labs": json.dumps({"HbA1c": 6.8}),
            "baseline": json.dumps({"HR": 75, "SpO2": 97, "RR": 16, "SysBP": 130, "DiaBP": 85})
        },
        {
            "patient_id": "P-003",
            "age": 71,
            "history": json.dumps(["COPD", "Hypertension"]),
            "medications": json.dumps(["Albuterol", "Lisinopril"]),
            "recent_labs": json.dumps({"pH": 7.36, "pCO2": 45}),
            "baseline": json.dumps({"HR": 85, "SpO2": 94, "RR": 18, "SysBP": 135, "DiaBP": 85})
        },
        {
            "patient_id": "P-004",
            "age": 58,
            "history": json.dumps(["Coronary Artery Disease", "Hyperlipidemia"]),
            "medications": json.dumps(["Atorvastatin", "Aspirin"]),
            "recent_labs": json.dumps({"Troponin": 0.01}),
            "baseline": json.dumps({"HR": 65, "SpO2": 99, "RR": 14, "SysBP": 115, "DiaBP": 75})
        },
        {
            "patient_id": "P-005",
            "age": 35,
            "history": json.dumps(["Asthma"]),
            "medications": json.dumps(["Fluticasone"]),
            "recent_labs": json.dumps({}),
            "baseline": json.dumps({"HR": 80, "SpO2": 97, "RR": 16, "SysBP": 120, "DiaBP": 80})
        },
        {
            "patient_id": "P-006",
            "age": 82,
            "history": json.dumps(["Dementia", "Osteoarthritis"]),
            "medications": json.dumps(["Donepezil", "Acetaminophen"]),
            "recent_labs": json.dumps({}),
            "baseline": json.dumps({"HR": 72, "SpO2": 96, "RR": 15, "SysBP": 125, "DiaBP": 82})
        }
    ]
    return pd.DataFrame(patients)

def generate_vitals_stream(seed=42, minutes=60):
    np.random.seed(seed)
    start_time = datetime(2026, 1, 1, 8, 0, 0)
    
    records = []
    for t in range(minutes):
        current_time = start_time + timedelta(minutes=t)
        
        # P-001: Stable
        records.append({
            "patient_id": "P-001",
            "timestamp": current_time,
            "heart_rate_bpm": int(np.random.normal(70, 2)),
            "spo2_percent": int(np.clip(np.random.normal(98, 1), 0, 100)),
            "respiratory_rate_bpm": int(np.random.normal(14, 1)),
            "systolic_bp_mmhg": int(np.random.normal(120, 3)),
            "diastolic_bp_mmhg": int(np.random.normal(80, 2)),
            "source": "monitor"
        })
        
        # P-002: Noisy SpO2 (mostly 97, but random drops for 1 min)
        spo2 = 97
        if t % 15 == 0 and t > 0:
            spo2 = 85 # sudden noise drop
        records.append({
            "patient_id": "P-002",
            "timestamp": current_time,
            "heart_rate_bpm": int(np.random.normal(75, 2)),
            "spo2_percent": spo2,
            "respiratory_rate_bpm": int(np.random.normal(16, 1)),
            "systolic_bp_mmhg": int(np.random.normal(130, 3)),
            "diastolic_bp_mmhg": int(np.random.normal(85, 2)),
            "source": "monitor"
        })
        
        # P-003: Respiratory Deterioration (starts min 20, SpO2 down, RR up)
        spo2 = 94
        rr = 18
        if t >= 20:
            spo2 -= int((t - 20) * 0.3)
            rr += int((t - 20) * 0.4)
            spo2 = max(80, spo2)
            rr = min(35, rr)
        records.append({
            "patient_id": "P-003",
            "timestamp": current_time,
            "heart_rate_bpm": int(np.random.normal(85, 2)),
            "spo2_percent": spo2,
            "respiratory_rate_bpm": rr,
            "systolic_bp_mmhg": int(np.random.normal(135, 3)),
            "diastolic_bp_mmhg": int(np.random.normal(85, 2)),
            "source": "monitor"
        })
        
        # P-004: Cardiovascular Deterioration (starts min 15, HR up, BP down)
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
        records.append({
            "patient_id": "P-004",
            "timestamp": current_time,
            "heart_rate_bpm": hr,
            "spo2_percent": int(np.clip(np.random.normal(99, 1), 0, 100)),
            "respiratory_rate_bpm": int(np.random.normal(14, 1)),
            "systolic_bp_mmhg": sys_bp,
            "diastolic_bp_mmhg": dia_bp,
            "source": "monitor"
        })
        
        # P-005: Recovery after alert (starts min 10 deterioration, recovers min 30)
        hr = 80
        spo2 = 97
        if 10 <= t < 30:
            hr += int((t - 10) * 1.2)
            spo2 -= int((t - 10) * 0.5)
        elif t >= 30:
            hr = 80 + max(0, int(24 - (t - 30) * 2))
            spo2 = 87 + min(10, int((t - 30) * 1))
        records.append({
            "patient_id": "P-005",
            "timestamp": current_time,
            "heart_rate_bpm": hr,
            "spo2_percent": spo2,
            "respiratory_rate_bpm": int(np.random.normal(16, 1)),
            "systolic_bp_mmhg": int(np.random.normal(120, 3)),
            "diastolic_bp_mmhg": int(np.random.normal(80, 2)),
            "source": "monitor"
        })
        
        # P-006: Missing Data (SpO2 drops out at min 25)
        spo2 = int(np.clip(np.random.normal(96, 1), 0, 100))
        if t >= 25:
            spo2 = np.nan
        records.append({
            "patient_id": "P-006",
            "timestamp": current_time,
            "heart_rate_bpm": int(np.random.normal(72, 2)),
            "spo2_percent": spo2,
            "respiratory_rate_bpm": int(np.random.normal(15, 1)),
            "systolic_bp_mmhg": int(np.random.normal(125, 3)),
            "diastolic_bp_mmhg": int(np.random.normal(82, 2)),
            "source": "monitor"
        })
        
    return pd.DataFrame(records)

if __name__ == "__main__":
    print("Generating synthetic data...")
    patients_df = generate_patients()
    patients_df.to_csv("patients.csv", index=False)
    
    vitals_df = generate_vitals_stream()
    vitals_df.to_csv("vitals_stream.csv", index=False)
    print("Generated patients.csv and vitals_stream.csv successfully.")
