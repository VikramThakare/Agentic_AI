import streamlit as st
import pandas as pd
import sqlite3
import time
from datetime import datetime
from ingestion import DataIngestor
from state import PatientStateManager
from audit import AuditLogger
import plotly.express as px
import db_setup
import json

# --- Config & Init ---
st.set_page_config(page_title="Agentic Clinical Copilot", layout="wide")

DB_NAME = "copilot.db"

@st.cache_resource
def init_system():
    db_setup.init_db()
    ingestor = DataIngestor()
    ingestor.load_patients()
    df = pd.read_csv("vitals_stream.csv")
    return df

stream_df = init_system()

# --- Session State ---
if 'stream_idx' not in st.session_state:
    st.session_state.stream_idx = 0 
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False
if 'selected_patient' not in st.session_state:
    st.session_state.selected_patient = "P-001"

# --- Helper Functions ---
def fetch_data(query):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def advance_stream():
    if st.session_state.stream_idx >= 60:
        st.session_state.is_playing = False
        return
        
    ingestor = DataIngestor()
    state_manager = PatientStateManager()
    audit = AuditLogger()
    
    # Process 6 readings (one for each patient at this minute)
    start_row = st.session_state.stream_idx * 6
    end_row = start_row + 6
    
    current_batch = stream_df.iloc[start_row:end_row]
    
    for _, row in current_batch.iterrows():
        reading_dict = row.to_dict()
        reading_id = ingestor.ingest_reading(reading_dict)
        state_manager.update_state(reading_id, reading_dict['patient_id'])
        
    ingestor.close()
    state_manager.close()
    audit.close()
    
    st.session_state.stream_idx += 1

# --- UI Sidebar ---
with st.sidebar:
    st.header("Stream Controls")
    
    st.write(f"**Simulated Minute:** {st.session_state.stream_idx} / 60")
    
    col1, col2, col3 = st.columns(3)
    if col1.button("▶ Play", disabled=st.session_state.is_playing):
        st.session_state.is_playing = True
        st.rerun()
    if col2.button("⏸ Pause", disabled=not st.session_state.is_playing):
        st.session_state.is_playing = False
        st.rerun()
    if col3.button("Step"):
        advance_stream()
        st.rerun()
        
    st.markdown("---")
    st.info("**Disclaimer:** Educational prototype only. Not a medical device.")

# Handle Auto-play
if st.session_state.is_playing:
    advance_stream()
    time.sleep(1.0) # 1 second per tick
    st.rerun()

# --- Main Dashboard ---
st.title("Clinical Deterioration & Escalation Copilot")

# 1. Cohort Overview
st.subheader("Cohort Overview")
patients_df = fetch_data("""
    SELECT p.patient_id, p.age, ps.risk_category, ps.risk_score, ps.updated_at, ps.active_alert_id
    FROM patients p
    JOIN patient_states ps ON p.patient_id = ps.patient_id
    ORDER BY ps.risk_score DESC
""")

# Styling the dataframe
def color_risk(val):
    if pd.isna(val): return ''
    color = '#ff4b4b' if val == 'critical' else '#ff8c00' if val == 'high' else '#ffcc00' if val == 'moderate' else '#00cc66'
    return f'color: {color}'

if not patients_df.empty:
    st.dataframe(patients_df.style.applymap(color_risk, subset=['risk_category']), use_container_width=True, hide_index=True)

# 2. Alert Queue
st.subheader("Active Alert Queue")
alerts_df = fetch_data("""
    SELECT alert_id, patient_id, created_at, status, priority_score, recommendation_text
    FROM alerts
    WHERE status = 'active'
    ORDER BY priority_score DESC
""")

if not alerts_df.empty:
    for _, alert in alerts_df.iterrows():
        with st.expander(f"🚨 {alert['patient_id']} - Score: {alert['priority_score']} - {alert['created_at']}", expanded=True):
            st.write(f"**Recommendation:** {alert['recommendation_text']}")
            
            comment = st.text_input("Comment (Optional)", key=f"cmt_{alert['alert_id']}")
            
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                if st.button("Accept", key=f"acc_{alert['alert_id']}"):
                    audit = AuditLogger()
                    audit.record_clinician_action(alert['alert_id'], alert['patient_id'], "accepted", comment)
                    audit.close()
                    st.rerun()
            with c2:
                if st.button("Dismiss", key=f"dis_{alert['alert_id']}"):
                    audit = AuditLogger()
                    audit.record_clinician_action(alert['alert_id'], alert['patient_id'], "dismissed", comment)
                    audit.close()
                    st.rerun()
            with c3:
                if st.button("Defer", key=f"def_{alert['alert_id']}"):
                    audit = AuditLogger()
                    audit.record_clinician_action(alert['alert_id'], alert['patient_id'], "deferred", comment)
                    audit.close()
                    st.rerun()
            with c4:
                if st.button("Investigate", key=f"inv_{alert['alert_id']}"):
                    st.session_state.selected_patient = alert['patient_id']
                    audit = AuditLogger()
                    audit.record_clinician_action(alert['alert_id'], alert['patient_id'], "investigated", comment)
                    audit.close()
                    st.rerun()
else:
    st.success("No active alerts at this time.")

# 3. Patient Details
st.markdown("---")
st.subheader("Patient Detail View")

selected_patient = st.selectbox("Select Patient", patients_df['patient_id'].tolist() if not patients_df.empty else ["P-001"], index=patients_df['patient_id'].tolist().index(st.session_state.selected_patient) if not patients_df.empty and st.session_state.selected_patient in patients_df['patient_id'].tolist() else 0)
st.session_state.selected_patient = selected_patient

if selected_patient:
    patient_info = fetch_data(f"SELECT * FROM patients WHERE patient_id = '{selected_patient}'").iloc[0]
    
    col_ctx, col_chart = st.columns([1, 2])
    
    with col_ctx:
        st.markdown(f"#### **{patient_info['patient_id']}** (Age: {patient_info['age']})")
        st.write(f"**History:** {', '.join(json.loads(patient_info['history']))}")
        st.write(f"**Medications:** {', '.join(json.loads(patient_info['medications']))}")
        st.write(f"**Recent Labs:** {patient_info['recent_labs']}")
        st.write(f"**Baseline:** {patient_info['baseline']}")
        
    with col_chart:
        history_df = fetch_data(f"""
            SELECT timestamp, heart_rate_bpm, spo2_percent, respiratory_rate_bpm, systolic_bp_mmhg, diastolic_bp_mmhg
            FROM vital_readings
            WHERE patient_id = '{selected_patient}'
            ORDER BY timestamp ASC
        """)
        
        if not history_df.empty:
            st.write("**Vital Trends (Simulated Stream)**")
            fig = px.line(history_df, x='timestamp', y=['heart_rate_bpm', 'spo2_percent', 'respiratory_rate_bpm', 'systolic_bp_mmhg', 'diastolic_bp_mmhg'], 
                          labels={'value': 'Measurement', 'variable': 'Vital Sign'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available yet. Press 'Play' or 'Step' to begin ingestion.")
