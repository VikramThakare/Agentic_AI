import sqlite3
import uuid
import json
import pandas as pd
from datetime import datetime, timedelta

class AlertManager:
    def __init__(self, db_conn, trend_engine):
        self.conn = db_conn
        self.trend_engine = trend_engine
        
    def check_persistence(self, history_df):
        """Checks if the last 3 readings all indicate deterioration."""
        if len(history_df) < 3:
            return False, 0
            
        points_list = []
        for i in range(1, 4):
            latest_n = history_df.iloc[:len(history_df)-i+1]
            res = self.trend_engine.evaluate(latest_n)
            if res.get("status") != "deteriorating":
                return False, 0
            points_list.append(res.get("points", 0))
            
        return True, max(points_list)

    def process_trend(self, patient_id, history_df):
        """
        Applies persistence rule and cooldown logic.
        """
        is_persistent, max_points = self.check_persistence(history_df)
        
        if not is_persistent:
            return None # Persistence rule not met
            
        # Check cooldown
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT cooldown_until FROM alerts 
            WHERE patient_id = ? AND status IN ('active', 'accepted', 'investigated', 'deferred')
            ORDER BY created_at DESC LIMIT 1
        """, (patient_id,))
        row = cursor.fetchone()
        
        current_time_str = str(history_df.iloc[-1]['timestamp'])
        
        try:
            current_time = datetime.fromisoformat(current_time_str)
        except ValueError:
            current_time = pd.to_datetime(current_time_str).to_pydatetime()
            
        if row and row[0]:
            try:
                cooldown_until = datetime.fromisoformat(row[0])
            except ValueError:
                cooldown_until = pd.to_datetime(row[0]).to_pydatetime()
            
            if current_time < cooldown_until:
                # In cooldown, suppress alert
                return None
                
        # Generate Alert
        alert_id = "AL-" + str(uuid.uuid4())[:8]
        cooldown_period = 10 # 10 simulated minutes cooldown
        cooldown_until_dt = current_time + timedelta(minutes=cooldown_period)
        
        # Risk score calculation
        priority_score = max_points + 5 # 5 points for persistence
        risk_category = "critical" if priority_score >= 10 else "high"
        
        # Determine signals
        latest_res = self.trend_engine.evaluate(history_df.iloc[-1:])
        concerning_signals = latest_res.get('concerning_signals', [])
        
        # Invoke ClinicalEscalationAgent
        import asyncio
        from agent import ClinicalEscalationAgent
        
        agent = ClinicalEscalationAgent()
        
        # This blocks until the agent finishes (or falls back)
        structured_response = asyncio.run(
            agent.generate_recommendation(patient_id, priority_score, concerning_signals)
        )
        
        # Format the structured response for the dashboard
        rec_text = (
            f"**Recommendation:** {structured_response.get('recommendation', '')}\n\n"
            f"**Evidence:** {structured_response.get('evidence', '')}\n\n"
            f"**Context:** {structured_response.get('patient_context', '')}\n\n"
            f"**Protocol Consulted:** {structured_response.get('protocol_source', '')}\n\n"
            f"**Limitations:** {structured_response.get('limitations', '')}"
        )
            
        # Save alert
        cursor.execute("""
            INSERT INTO alerts (alert_id, patient_id, created_at, status, priority_score, trigger_summary, recommendation_text, cooldown_until)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            alert_id, 
            patient_id, 
            current_time.isoformat(), 
            "active", 
            priority_score, 
            json.dumps({"reason": "persistent_multi_signal", "window": 3, "signals": concerning_signals, "agent_structured": structured_response}), 
            rec_text,
            cooldown_until_dt.isoformat()
        ))
        
        # We optionally log the protocol retrieval evidence if it was found
        protocol_doc = structured_response.get('protocol_source', '')
        if protocol_doc and protocol_doc != "System Fallback":
            cursor.execute("""
                INSERT INTO evidence_records (alert_id, patient_id, document_id, section_title, text_excerpt, retrieval_timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                alert_id,
                patient_id,
                protocol_doc,
                "Agentic Retrieval",
                json.dumps(structured_response),
                current_time.isoformat()
            ))
            
        # Log to Audit Trail
        from audit import AuditLogger
        audit = AuditLogger(self.conn.execute("PRAGMA database_list").fetchone()[2] if hasattr(self.conn, 'execute') else "copilot.db")
        audit.conn = self.conn # Use existing transaction connection
        audit.log_event(
            patient_id, 
            alert_id, 
            "ALERT_GENERATED", 
            {
                "priority_score": priority_score,
                "signals": concerning_signals,
                "protocol_retrieved": protocol_doc,
                "recommendation_summary": structured_response.get('summary', '')
            }
        )
        
        self.conn.commit()
        return {
            "alert_id": alert_id,
            "priority_score": priority_score,
            "risk_category": risk_category
        }
