const API_URL = 'http://127.0.0.1:8000';
let simulationInterval = null;
let globalResetInterval = null;

// Initial state for 5 patients
const patientsState = {
    'P-001': { hr: 70, spo2: 97, rr: 14, sys: 120, dia: 80, criticalTimer: null },
    'P-002': { hr: 75, spo2: 98, rr: 16, sys: 125, dia: 82, criticalTimer: null },
    'P-003': { hr: 80, spo2: 96, rr: 18, sys: 130, dia: 85, criticalTimer: null },
    'P-004': { hr: 65, spo2: 99, rr: 12, sys: 115, dia: 75, criticalTimer: null },
    'P-005': { hr: 72, spo2: 97, rr: 15, sys: 122, dia: 78, criticalTimer: null }
};

function generateNextVitals(patientId) {
    const state = patientsState[patientId];
    // Random walk for vitals
    state.hr = Math.max(40, Math.min(180, state.hr + (Math.random() * 4 - 2)));
    state.spo2 = Math.max(70, Math.min(100, state.spo2 + (Math.random() * 2 - 0.5))); // bias slightly up to recover
    state.rr = Math.max(8, Math.min(40, state.rr + (Math.random() * 2 - 1)));
    state.sys = Math.max(70, Math.min(200, state.sys + (Math.random() * 6 - 3)));
    state.dia = Math.max(40, Math.min(120, state.dia + (Math.random() * 4 - 2)));
    
    // To ensure we generate some alerts, let's randomly sometimes drop vitals significantly
    // The backend rules require:
    // Respiratory: SpO2 < 92 AND RR > 22
    // Cardiovascular: HR > 120 AND Sys BP < 90
    if (Math.random() < 0.005) { // 0.5% chance to simulate Respiratory failure
        state.spo2 = 85;
        state.rr = 28;
    } else if (Math.random() < 0.005) { // 0.5% chance to simulate Cardiovascular failure
        state.hr = 135;
        state.sys = 80;
    }
    
    return {
        patient_id: patientId,
        timestamp: new Date().toISOString(),
        heart_rate_bpm: Math.round(state.hr),
        spo2_percent: Math.round(state.spo2),
        respiratory_rate_bpm: Math.round(state.rr),
        systolic_bp_mmhg: Math.round(state.sys),
        diastolic_bp_mmhg: Math.round(state.dia)
    };
}

document.getElementById('start-simulation').addEventListener('click', async () => {
    const btn = document.getElementById('start-simulation');
    
    if (simulationInterval) {
        clearInterval(simulationInterval);
        simulationInterval = null;
        if (globalResetInterval) clearInterval(globalResetInterval);
        globalResetInterval = null;
        btn.textContent = "Start Simulation";
        document.getElementById('sim-status').textContent = "Simulation paused.";
        return;
    }
    
    btn.textContent = "Stop Simulation";
    const statusText = document.getElementById('sim-status');
    statusText.textContent = "Live infinite stream running... Alerts expire after 30s.";
    
    // Clear only if this is a fresh start (optional, we could leave existing alerts)
    // document.getElementById('alerts-container').innerHTML = ''; 

    // Global reset every 30 seconds
    globalResetInterval = setInterval(() => {
        document.getElementById('alerts-container').innerHTML = '';
        const patientIds = Object.keys(patientsState);
        patientIds.forEach(pid => {
            document.getElementById(`${pid}-status`).textContent = "Monitoring";
            document.getElementById(`${pid}-status`).className = "status-badge stable";
            document.getElementById(`card-${pid}`).style.borderColor = "";
            document.getElementById(`card-${pid}`).style.boxShadow = "";
        });
    }, 30000);

    let tick = 0;
    
    // Loop every 1 second
    simulationInterval = setInterval(async () => {
        tick++;
        statusText.textContent = `Tick: ${tick} (Continuous Stream)`;
        
        const patientIds = Object.keys(patientsState);
        
        // Fire off the API requests for this tick concurrently
        patientIds.forEach(pid => {
            const row = generateNextVitals(pid);
            
            // Update UI instantly for the dashboard grid
            document.getElementById(`${row.patient_id}-hr`).textContent = row.heart_rate_bpm;
            document.getElementById(`${row.patient_id}-spo2`).textContent = row.spo2_percent;
            document.getElementById(`${row.patient_id}-rr`).textContent = row.respiratory_rate_bpm;
            document.getElementById(`${row.patient_id}-bp`).textContent = `${row.systolic_bp_mmhg}/${row.diastolic_bp_mmhg}`;

            // Call Backend LangGraph
            fetch(`${API_URL}/vitals/stream`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(row)
            }).then(res => res.json()).then(data => {
                // If LangGraph paused the graph, it means the rules triggered and AI replied
                if (data.requires_human_review || data.escalation_available) {
                    // Mark card red
                    document.getElementById(`${row.patient_id}-status`).textContent = "CRITICAL";
                    document.getElementById(`${row.patient_id}-status`).className = "status-badge critical";
                    document.getElementById(`card-${row.patient_id}`).style.borderColor = "#ef4444";
                    document.getElementById(`card-${row.patient_id}`).style.boxShadow = "0 0 15px rgba(239, 68, 68, 0.4)";

                    // Output the actual AI response
                    renderAlert(data);
                }
            }).catch(err => console.error(err));
        });
        
    }, 1000); 
});

function renderAlert(data) {
    const container = document.getElementById('alerts-container');
    const div = document.createElement('div');
    div.className = "alert-card";
    
    let aiReasoningHtml = "";
    
    try {
        // The LLM output might be a stringified JSON inside the escalation_data
        let parsedData = data.escalation_data;
        if (typeof parsedData === 'string') {
            // strip markdown code block syntax if it exists
            const cleanStr = parsedData.replace(/^```json\s*/, '').replace(/```\s*$/, '');
            parsedData = JSON.parse(cleanStr);
        }

        // Check if we successfully parsed the expected schema
        if (parsedData && parsedData.severity_tier) {
            let color = parsedData.severity_tier.toLowerCase() === 'critical' ? '#ef4444' : '#f59e0b';
            
            aiReasoningHtml = `
                <div style="margin-top: 1rem; background: rgba(0,0,0,0.3); padding: 1.5rem; border-radius: 12px; border-left: 4px solid ${color};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <span style="color: ${color}; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 0.85rem;">
                            SEVERITY: ${parsedData.severity_tier}
                        </span>
                        <span style="background: rgba(255,255,255,0.1); padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 0.9rem;">
                            Risk Score: ${parsedData.risk_score} / 10
                        </span>
                    </div>
                    
                    <p style="color: #e2e8f0; line-height: 1.6; font-size: 1.05rem; margin-bottom: 1.5rem;">
                        ${parsedData.plain_language_explanation}
                    </p>
                    
                    <h4 style="color: #c4b5fd; margin-bottom: 0.75rem; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.5px;">Recommended Actions</h4>
                    <ul style="color: #cbd5e1; list-style-type: none; padding-left: 0; margin: 0; display: flex; flex-direction: column; gap: 8px;">
                        ${parsedData.recommended_actions.map(action => `
                            <li style="display: flex; align-items: start;">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" style="margin-right: 10px; margin-top: 2px; flex-shrink: 0;">
                                    <polyline points="9 18 15 12 9 6"></polyline>
                                </svg>
                                <span>${action}</span>
                            </li>
                        `).join('')}
                    </ul>
                </div>
            `;
        } else {
            throw new Error("Not a structured JSON");
        }
    } catch (e) {
        // Fallback if parsing fails or structure is different
        let fallbackText = typeof data.escalation_data === 'string' ? data.escalation_data : JSON.stringify(data.escalation_data, null, 2);
        aiReasoningHtml = `
            <div style="margin-top: 1rem; background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 8px; border-left: 3px solid #8b5cf6;">
                <strong style="color: #c4b5fd;">Groq LLM Output:</strong><br>
                <pre style="white-space: pre-wrap; font-family: inherit; margin-top: 0.5rem; color: #e2e8f0;">${fallbackText}</pre>
            </div>
        `;
    }

    div.innerHTML = `
        <h3 style="color: #ef4444;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 8px;">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line x1="12" y1="9" x2="12" y2="13"></line>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
            ${data.patient_id} - RAG Brain Escalation Triggered
        </h3>
        <p class="alert-stat"><strong>Graph Status:</strong> Paused waiting for Human-in-Loop</p>
        ${aiReasoningHtml}
        
        <div style="margin-top: 1.5rem; display: flex; gap: 12px; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1);">
            <button onclick="submitDecision('${data.patient_id}', 'accept')" style="background: #10b981; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 0.95rem; transition: background 0.2s;">
                Approve Protocol
            </button>
            <button onclick="submitDecision('${data.patient_id}', 'dismiss')" style="background: rgba(255,255,255,0.15); color: #cbd5e1; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 0.95rem; transition: background 0.2s;">
                Dismiss Alert
            </button>
        </div>
    `;
    
    // Clear previous alerts so we only show the absolute latest one
    container.innerHTML = '';
    container.appendChild(div);
}

// Function to handle clinician decision and resume LangGraph thread
window.submitDecision = async (patientId, decision) => {
    try {
        const res = await fetch(`${API_URL}/alerts/${patientId}/decision`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ decision: decision, clinician_id: 'Dr. Smith' })
        });
        
        if (res.ok) {
            console.log(`Decision '${decision}' submitted for ${patientId}`);
            // Clear the alert from the UI manually
            document.getElementById('alerts-container').innerHTML = '';
            document.getElementById(`${patientId}-status`).textContent = "Monitoring";
            document.getElementById(`${patientId}-status`).className = "status-badge stable";
            document.getElementById(`card-${patientId}`).style.borderColor = "";
            document.getElementById(`card-${patientId}`).style.boxShadow = "";
        } else {
            console.error("Failed to submit decision");
        }
    } catch (e) {
        console.error("Error submitting decision:", e);
    }
};
