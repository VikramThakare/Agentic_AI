import sqlite3
from datetime import datetime
import json

DB_NAME = "copilot.db"

class AuditLogger:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)

    def log_event(self, patient_id, alert_id, event_type, event_data_dict):
        """
        Logs an audit event to the database.
        event_type: 'ALERT_GENERATED', 'CLINICIAN_ACTION', 'SYSTEM_INFO'
        """
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO audit_events (alert_id, patient_id, event_type, event_data, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (
            alert_id, 
            patient_id, 
            event_type, 
            json.dumps(event_data_dict), 
            now
        ))
        self.conn.commit()

    def record_clinician_action(self, alert_id, patient_id, action, comment=""):
        """
        Records a clinician's action (accept, dismiss, defer, investigate) on an alert.
        Updates the alert status as well.
        """
        cursor = self.conn.cursor()
        
        # 1. Update alert status
        now = datetime.now().isoformat()
        cursor.execute("""
            UPDATE alerts
            SET status = ?
            WHERE alert_id = ?
        """, (action.lower(), alert_id))
        
        # 2. Update patient state if the alert is resolved/dismissed/accepted (to remove it from active)
        if action.lower() in ['dismissed', 'accepted']:
            cursor.execute("""
                UPDATE patient_states
                SET active_alert_id = NULL
                WHERE active_alert_id = ?
            """, (alert_id,))
            
        self.conn.commit()
        
        # 3. Log to audit trail
        self.log_event(
            patient_id=patient_id,
            alert_id=alert_id,
            event_type="CLINICIAN_ACTION",
            event_data_dict={"action": action, "comment": comment, "user": "clinician_demo"}
        )

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    logger = AuditLogger()
    print("AuditLogger initialized.")
    logger.close()
