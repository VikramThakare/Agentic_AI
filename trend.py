import yaml
import pandas as pd
import numpy as np

class TrendEngine:
    def __init__(self, config_path="config/thresholds.yaml"):
        with open(config_path, 'r') as f:
            self.thresholds = yaml.safe_load(f)
            
    def is_concerning(self, vital_name, current_val, baseline_val=None):
        """
        Checks if a current value is concerning (moderate, high, or critical).
        """
        if pd.isna(current_val):
            return False, 0
            
        th = self.thresholds.get(vital_name, {})
        if not th:
            return False, 0
            
        concerning = False
        direction = 0 # -1 for low, 1 for high
        
        # SpO2 specific (lower is worse)
        if vital_name == 'spo2_percent':
            if current_val <= th.get('critical', 85): concerning = True; direction = -1
            elif current_val <= th.get('high', 90): concerning = True; direction = -1
            elif current_val <= th.get('moderate', 94): concerning = True; direction = -1
            return concerning, direction

        # Other vitals
        if 'critical' in th and current_val >= th['critical']: concerning = True; direction = 1
        elif 'high' in th and current_val >= th['high']: concerning = True; direction = 1
        elif 'moderate' in th and current_val >= th['moderate']: concerning = True; direction = 1
        elif 'low' in th and current_val <= th['low']: concerning = True; direction = -1
            
        return concerning, direction
        
    def evaluate(self, history_df):
        """
        Evaluates the rolling window of a patient's vital history (e.g., last 5 readings).
        Returns a dictionary with trend features and whether it's a multi-signal deterioration.
        """
        if history_df.empty:
            return {"status": "insufficient_data"}
            
        latest = history_df.iloc[-1]
        concerning_signals = []
        
        vitals_to_check = ['heart_rate_bpm', 'spo2_percent', 'respiratory_rate_bpm', 'systolic_bp_mmhg', 'diastolic_bp_mmhg']
        
        for vital in vitals_to_check:
            val = latest.get(vital)
            is_conc, _ = self.is_concerning(vital, val)
            if is_conc:
                concerning_signals.append(vital)
                
        is_multi_signal = len(concerning_signals) >= 2
        points = len(concerning_signals) * 2
        
        if is_multi_signal:
            points += 3 # bonus for multi-signal agreement
            
        return {
            "status": "deteriorating" if is_multi_signal else "stable" if len(concerning_signals) == 0 else "single_signal",
            "concerning_signals": concerning_signals,
            "points": points,
            "latest_timestamp": latest['timestamp']
        }
