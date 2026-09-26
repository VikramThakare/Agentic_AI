// Initialize Feather Icons
feather.replace();

// Mock Patient Data
// We'll populate this dynamically from the backend
let patientsData = {};

// Fetch patients list on load
async function fetchPatients() {
    try {
        const res = await fetch('http://127.0.0.1:8000/api/patients');
        const patientsList = await res.json();
        
        patientsData = {};
        patientsList.forEach((p, idx) => {
            const colors = ['blue', 'teal', 'purple', 'red', 'green', 'orange'];
            const color = colors[idx % colors.length];
            
            const realNames = ["Ava Patel", "Noah Williams", "Maya Singh", "Ethan Chen", "Olivia Smith", "Liam Garcia"];
            const name = p.name || (idx < 6 ? realNames[idx] : 'Patient ' + p.patient_id);
            const initials = name.split(' ').map(n => n[0]).join('').substring(0, 2) || 'XX';
            
            const mockDob = `${Math.floor(Math.random() * 28) + 1} ${['Jan','Feb','Mar','Apr','May','Jun'][Math.floor(Math.random()*6)]} 19${Math.floor(Math.random()*40)+50}`;
            const mockPhone = `+1 (555) 014-${Math.floor(Math.random()*9000)+1000}`;
            
            patientsData[p.patient_id] = {
                name: name,
                initials: initials,
                avatarColor: color,
                id: p.patient_id,
                room: p.room || ('10' + (idx+1)),
                status: 'Stable',
                statusClass: 'stable',
                statusColor: 'green',
                hr: '--',
                spo2: '--',
                bp: '--/--',
                dob: p.dob || mockDob,
                gender: p.gender || (Math.random() > 0.5 ? 'Male' : 'Female'),
                phone: p.phone || mockPhone,
                email: p.email || `patient.${p.patient_id.toLowerCase()}@example.com`,
                emergency: p.emergency || 'Relative Contact',
                history: p.history || 'No significant history',
                medications: p.medications || 'None',
                hrData: new Array(60).fill(70),
                spo2Data: new Array(60).fill(98),
                bpData: new Array(60).fill(120),
                escalation: null
            };
        });
        
        renderOverviewTable();
        renderPatientsListTable();
        updateDashboardMetrics();
    } catch (err) {
        console.error("Failed to load patients list", err);
    }
}
fetchPatients();

async function addNewPatientPrompt() {
    const pid = prompt("Enter Patient ID (e.g. P-007):", "P-007");
    if (!pid) return;
    const name = prompt("Enter Patient Name:", "John Doe") || "";
    const age = prompt("Enter Patient Age:", "45");
    const gender = prompt("Enter Gender (Male/Female/Other):", "Male") || "";
    const dob = prompt("Enter DOB (e.g. 14 Mar 1988):", "14 Mar 1988") || "";
    const phone = prompt("Enter Phone:", "+1 (555) 123-4567") || "";
    const email = prompt("Enter Email:", "john@example.com") || "";
    const emergency = prompt("Enter Emergency Contact:", "Jane Doe") || "";
    const room = prompt("Enter Room/Bed:", "107 / Bed 1") || "";
    const history = prompt("Enter History:", "No major history");
    const meds = prompt("Enter Medications:", "None");
    
    try {
        const response = await fetch('http://127.0.0.1:8000/api/patients', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                patient_id: pid,
                name: name,
                age: parseInt(age),
                gender: gender,
                dob: dob,
                phone: phone,
                email: email,
                emergency: emergency,
                room: room,
                history: history,
                medications: meds
            })
        });
        const resData = await response.json();
        alert(resData.message);
        
        // Refresh everything
        if (simulationActive) {
            toggleSimulation(); // stop
        }
        simulationData = []; // clear cache so we fetch new stream data
        await fetchPatients();
        
    } catch (err) {
        console.error(err);
        alert("Failed to add patient.");
    }
}

async function removePatientPrompt() {
    const pid = prompt("Enter Patient ID to remove (e.g. P-007):");
    if (!pid) return;
    
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/patients/${pid}`, {
            method: 'DELETE',
        });
        const resData = await response.json();
        alert(resData.message || "Patient removed successfully");
        
        if (simulationActive) toggleSimulation(); // stop
        fetchPatients();
        simulationData = []; // clear cache
    } catch (err) {
        console.error("Failed to remove patient:", err);
        alert("Error removing patient. See console.");
    }
}

async function editPatientPrompt() {
    const pid = prompt("Enter Patient ID to edit (e.g. P-001):");
    if (!pid || !patientsData[pid]) {
        alert("Patient not found locally.");
        return;
    }
    
    const currentHistory = patientsData[pid].history || "None";
    const currentMeds = patientsData[pid].medications || "None";
    
    const history = prompt("Edit History:", currentHistory);
    if (history === null) return;
    
    const meds = prompt("Edit Medications:", currentMeds);
    if (meds === null) return;
    
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/patients/${pid}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                history: history,
                medications: meds
            })
        });
        const resData = await response.json();
        alert(resData.message || "Patient updated successfully");
        
        if (simulationActive) toggleSimulation(); // stop
        fetchPatients();
        simulationData = []; // clear cache
    } catch (err) {
        console.error("Failed to edit patient:", err);
        alert("Error editing patient. See console.");
    }
}

function renderOverviewTable() {
    const tbody = document.getElementById('patients-table-body');
    if (!tbody) return;
    
    let html = '';
    for (const [pid, p] of Object.entries(patientsData)) {
        html += `
        <tr onclick="switchView('patient-detail', '${pid}')">
            <td>
                <div class="patient-cell">
                    <span class="avatar small ${p.avatarColor}">${p.initials}</span>
                    <span class="patient-name">${p.name}</span>
                </div>
            </td>
            <td class="text-secondary">${p.id}</td>
            <td class="text-secondary">${p.room}</td>
            <td>
                <div class="vital-cell">
                    <div class="vital-val"><strong id="overview-hr-${pid}">${p.hr}</strong> <small>bpm</small></div>
                    <svg class="sparkline green" viewBox="0 0 50 15"><path d="M0,10 L10,8 L20,12 L30,2 L40,10 L50,8"></path></svg>
                </div>
            </td>
            <td>
                <div class="vital-cell">
                    <div class="vital-val"><strong id="overview-spo2-${pid}">${p.spo2}%</strong></div>
                    <svg class="sparkline green" viewBox="0 0 50 15"><path d="M0,8 L15,10 L25,5 L35,9 L50,8"></path></svg>
                </div>
            </td>
            <td><span class="status-badge ${p.statusClass}" id="overview-status-${pid}"><span class="dot"></span> ${p.status}</span></td>
            <td class="text-secondary">Just now</td>
            <td><i data-feather="more-vertical" class="text-secondary"></i></td>
        </tr>`;
    }
    tbody.innerHTML = html;
    feather.replace();
}

function updateDashboardMetrics() {
    let total = 0, stable = 0, attention = 0, critical = 0;
    for (const p of Object.values(patientsData)) {
        total++;
        if (p.statusClass === 'stable') stable++;
        else if (p.statusClass === 'critical') critical++;
        else attention++; // warning/attention
    }
    
    const elTotal = document.getElementById('metric-total-patients');
    const elStable = document.getElementById('metric-stable');
    const elCritical = document.getElementById('metric-critical');
    
    if (elTotal) elTotal.innerText = total;
    if (elStable) elStable.innerText = stable;
    if (elCritical) elCritical.innerText = critical;
    
    renderAlertsTable();
    renderRecentAlertsWidget();
}

function renderRecentAlertsWidget() {
    const list = document.getElementById('recent-alerts-list');
    if (!list) return;
    
    let html = '';
    for (const [pid, p] of Object.entries(patientsData)) {
        if (p.escalation) {
            // Determine icon and color based on escalation summary
            let icon = 'activity';
            let color = 'red';
            let iconHtml = `<i data-feather="${icon}" class="${color}-text"></i>`;
            
            const summaryLower = (p.escalation.summary || '').toLowerCase();
            if (summaryLower.includes('spo2') || summaryLower.includes('oxygen')) {
                color = 'orange';
                iconHtml = `<span class="element-icon ${color}-text">O₂</span>`;
            }
            
            html += `
            <div class="alert-item" style="cursor: pointer;" onclick="switchView('patient-detail', '${pid}')">
                <div class="alert-icon-wrapper ${color}-bg">
                    ${iconHtml}
                </div>
                <div class="alert-details">
                    <div class="alert-title ${color}-text">${p.name}</div>
                    <div class="alert-desc">${p.escalation.summary || 'Critical alert generated'}</div>
                    <div class="alert-time">Just now</div>
                </div>
            </div>`;
        }
    }
    
    if (html === '') {
        html = '<div style="padding: 20px; text-align: center; color: #64748b; font-size: 0.9em;">No recent alerts.</div>';
    }
    
    list.innerHTML = html;
    feather.replace();
}

function renderAlertsTable() {
    const tbody = document.getElementById('alerts-table-body');
    if (!tbody) return;
    
    let html = '';
    for (const [pid, p] of Object.entries(patientsData)) {
        if (p.escalation) {
            html += `
            <tr>
                <td>
                    <div class="patient-cell">
                        <span class="avatar small ${p.avatarColor}">${p.initials}</span>
                        <span class="patient-name">${p.name}</span>
                    </div>
                </td>
                <td><span class="status-badge ${p.statusClass}"><span class="dot"></span> ${p.status}</span></td>
                <td>${p.escalation.summary || 'Critical intervention required'}</td>
                <td>
                    <button class="btn primary-btn" onclick="switchView('patient-detail', '${pid}')">Review</button>
                </td>
            </tr>`;
        }
    }
    if (html === '') {
        html = '<tr><td colspan="4" style="text-align: center; color: #64748b; padding: 20px;">No active alerts.</td></tr>';
    }
    tbody.innerHTML = html;
}

function renderPatientsListTable() {
    const tbody = document.getElementById('patients-list-table-body');
    if (!tbody) return;
    
    let html = '';
    for (const [pid, p] of Object.entries(patientsData)) {
        // approximate age from mock dob (e.g. "14 Mar 1988")
        const yearStr = p.dob.substring(p.dob.length - 4);
        const age = yearStr ? new Date().getFullYear() - parseInt(yearStr) : '--';
        
        html += `
        <tr>
            <td>
                <div class="patient-cell">
                    <span class="avatar small ${p.avatarColor}">${p.initials}</span>
                    <span class="patient-name">${p.name}</span>
                </div>
            </td>
            <td class="text-secondary">${p.id}</td>
            <td>${age} <span class="text-secondary" style="font-size: 0.85em;">(${p.dob})</span></td>
            <td>${p.gender}</td>
            <td>${p.room} / Bed ${Math.floor(Math.random() * 4) + 1}</td>
            <td>
                <div>${p.emergency}</div>
                <div class="text-secondary" style="font-size: 0.85em;">${p.phone}</div>
            </td>
            <td>
                <button class="btn outline-btn" onclick="switchView('patient-detail', '${pid}')">
                    <i data-feather="activity"></i> Vitals
                </button>
            </td>
        </tr>`;
    }
    tbody.innerHTML = html;
    feather.replace();
}

// Simulation state
let simulationActive = false;
let simulationInterval = null;
let simulationData = [];
let simIndex = 0;

async function toggleSimulation() {
    const btn = document.getElementById('toggle-sim-btn');
    const statusText = document.getElementById('sim-status');
    
    if (simulationActive) {
        // Stop
        simulationActive = false;
        clearInterval(simulationInterval);
        btn.innerHTML = '<i data-feather="play"></i> Start Simulation';
        statusText.innerText = 'Synthetic data generation - Idle';
        btn.classList.remove('outline-btn');
        btn.classList.add('primary-btn');
    } else {
        // Start
        simulationActive = true;
        btn.innerHTML = '<i data-feather="square"></i> Stop Simulation';
        statusText.innerText = 'Synthetic data generation - Active';
        btn.classList.remove('primary-btn');
        btn.classList.add('outline-btn');
        
        if (simulationData.length === 0) {
            try {
                const res = await fetch('http://127.0.0.1:8000/api/simulate/data');
                simulationData = await res.json();
                simIndex = 0;
            } catch (err) {
                console.error("Failed to load simulation data:", err);
                statusText.innerText = 'Synthetic data generation - Error (Is server running?)';
                toggleSimulation();
                return;
            }
        }
        
        simulationInterval = setInterval(processNextSimulationData, 1000); // 1 tick = 1 sec
    }
    feather.replace();
}

async function processNextSimulationData() {
    if (!simulationData || simIndex >= simulationData.length) {
        // Fetch next batch to keep the stream going infinitely
        try {
            const res = await fetch('http://127.0.0.1:8000/api/simulate/data');
            simulationData = await res.json();
            simIndex = 0;
            if (!simulationData || simulationData.length === 0) {
                toggleSimulation(); // Stop if genuinely no data
                return;
            }
        } catch (err) {
            console.error("Failed to load more simulation data:", err);
            toggleSimulation(); // Stop on error
            return;
        }
    }
    
    // Group by timestamp: Process all readings for the current tick together
    const currentTimestamp = simulationData[simIndex].timestamp;
    
    while (simIndex < simulationData.length && simulationData[simIndex].timestamp === currentTimestamp) {
        const currentRecord = simulationData[simIndex];
        simIndex++;
        
        // Send to backend LangGraph
        try {
            const response = await fetch('http://127.0.0.1:8000/vitals/stream', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(currentRecord)
            });
            const result = await response.json();
            
            // Update local mock data to reflect changes
            const pid = currentRecord.patient_id;
            if (patientsData[pid]) {
                patientsData[pid].hr = currentRecord.heart_rate_bpm;
                patientsData[pid].spo2 = currentRecord.spo2_percent || '--';
                patientsData[pid].bp = `${currentRecord.systolic_bp_mmhg}/${currentRecord.diastolic_bp_mmhg}`;
                
                patientsData[pid].hrData.shift();
                patientsData[pid].hrData.push(currentRecord.heart_rate_bpm);
                
                if (currentRecord.spo2_percent) {
                    patientsData[pid].spo2Data.shift();
                    patientsData[pid].spo2Data.push(currentRecord.spo2_percent);
                }
                
                patientsData[pid].bpData.shift();
                patientsData[pid].bpData.push(currentRecord.systolic_bp_mmhg);
                
                if (result.escalation_data) {
                    patientsData[pid].escalation = result.escalation_data;
                    patientsData[pid].status = "Critical";
                    patientsData[pid].statusClass = "critical";
                    patientsData[pid].statusColor = "red";
                } else {
                    patientsData[pid].escalation = null;
                }
                
                // Update Overview Table DOM
                const overviewHr = document.getElementById(`overview-hr-${pid}`);
                if (overviewHr) overviewHr.innerText = patientsData[pid].hr;
                
                const overviewSpo2 = document.getElementById(`overview-spo2-${pid}`);
                if (overviewSpo2) overviewSpo2.innerText = `${patientsData[pid].spo2}%`;
                
                const overviewStatus = document.getElementById(`overview-status-${pid}`);
                if (overviewStatus) {
                    overviewStatus.innerHTML = `<span class="dot"></span> ${patientsData[pid].status}`;
                    overviewStatus.className = `status-badge ${patientsData[pid].statusClass}`;
                }
                
                updateDashboardMetrics();
                
                // Update Patient Detail View DOM if active
                const patientDetailView = document.getElementById('view-patient-detail');
                const currentProfileId = document.getElementById('profile-id').innerText;
                
                if (!patientDetailView.classList.contains('hidden-view') && currentProfileId === pid) {
                    populatePatientDetail(patientsData[pid]);
                }
            }
        } catch (err) {
            console.error("Failed to POST vitals:", err);
        }
    }
}

// View switching logic
function switchView(viewId, patientId = null) {
    // Hide all views
    document.querySelectorAll('.view').forEach(view => {
        view.classList.remove('active-view');
        view.classList.add('hidden-view');
    });

    // Update active state in sidebar
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    let targetView = viewId;
    if (viewId === 'patient-detail') {
        targetView = 'view-patient-detail';
        const patientNavItem = document.querySelector('[data-view="patients"]');
        if (patientNavItem) patientNavItem.classList.add('active');
        
        if (patientId && patientsData[patientId]) {
            populatePatientDetail(patientsData[patientId]);
        }
    } else if (viewId === 'overview') {
        targetView = 'view-overview';
        const overviewNavItem = document.querySelector('[data-view="overview"]');
        if (overviewNavItem) overviewNavItem.classList.add('active');
    } else if (viewId === 'alerts') {
        targetView = 'view-alerts';
        const alertsNavItem = document.querySelector('[data-view="alerts"]');
        if (alertsNavItem) alertsNavItem.classList.add('active');
        renderAlertsTable();
    } else if (viewId === 'patients-list') {
        targetView = 'view-patients-list';
        const patientNavItem = document.querySelector('[data-view="patients"]');
        if (patientNavItem) patientNavItem.classList.add('active');
        renderPatientsListTable();
    }

    // Show target view
    const viewElement = document.getElementById(targetView);
    if (viewElement) {
        viewElement.classList.remove('hidden-view');
        viewElement.classList.add('active-view');
    }
}

function populatePatientDetail(patient) {
    // Header & Meta
    document.getElementById('breadcrumb-patient-name').innerText = `/ ${patient.name}`;
    
    const profileAvatar = document.getElementById('profile-avatar');
    profileAvatar.innerText = patient.initials;
    profileAvatar.className = `avatar large ${patient.avatarColor}`;
    
    document.getElementById('profile-name').innerText = patient.name;
    document.getElementById('profile-id').innerText = patient.id;
    document.getElementById('profile-room').innerText = patient.room;
    
    const profileStatus = document.getElementById('profile-status');
    profileStatus.innerHTML = `<span class="dot"></span> ${patient.status}`;
    profileStatus.className = `status-badge ${patient.statusClass} compact`;
    
    // Vitals Cards
    document.getElementById('detail-hr-val').innerHTML = `${patient.hr} <small>bpm</small>`;
    document.getElementById('detail-spo2-val').innerText = `${patient.spo2}%`;
    document.getElementById('detail-bp-val').innerHTML = `${patient.bp} <small>mmHg</small>`;
    
    // Big Status Circle
    document.getElementById('detail-status-circle').className = `status-circle ${patient.statusColor}-bg`;
    const statusText = document.getElementById('detail-status-text');
    statusText.innerText = patient.status;
    statusText.className = `status-text ${patient.statusColor}-text`;
    
    // Personal Details
    document.getElementById('detail-dob').innerText = patient.dob;
    document.getElementById('detail-gender').innerText = patient.gender;
    document.getElementById('detail-phone').innerText = patient.phone;
    document.getElementById('detail-email').innerText = patient.email;
    document.getElementById('detail-emergency').innerText = patient.emergency;
    
    // Check if these elements exist, then populate
    const elHistory = document.getElementById('detail-history');
    if (elHistory) elHistory.innerText = patient.history;
    
    const elMeds = document.getElementById('detail-meds');
    if (elMeds) elMeds.innerText = patient.medications;
    
    // AI Escalation (RAG + Groq Output)
    const escalationPanel = document.getElementById('ai-escalation-panel');
    const ragOutput = document.getElementById('rag-output');
    const actionButtons = document.getElementById('human-loop-actions');
    
    if (patient.escalation && !patient.escalation.error) {
        escalationPanel.style.display = 'block';
        if (actionButtons) actionButtons.style.display = 'flex';
        
        let escalationHtml = `<strong>Risk Level:</strong> <span class="status-badge ${patient.escalation.severity_tier}">${patient.escalation.severity_tier}</span><br><br>`;
        escalationHtml += `<strong>Risk Score:</strong> ${patient.escalation.risk_score} / 10<br><br>`;
        escalationHtml += `<strong>Summary:</strong> ${patient.escalation.plain_language_explanation || 'No summary provided'}<br><br>`;
        
        if (patient.escalation.recommended_actions && patient.escalation.recommended_actions.length > 0) {
            escalationHtml += `<strong>Interventions:</strong><ul>`;
            patient.escalation.recommended_actions.forEach(item => {
                if(item.trim() !== "") {
                    escalationHtml += `<li>${item}</li>`;
                }
            });
            escalationHtml += `</ul>`;
        }
        ragOutput.innerHTML = escalationHtml;
    } else if (patient.escalation && patient.escalation.error) {
        escalationPanel.style.display = 'block';
        if (actionButtons) actionButtons.style.display = 'none';
        ragOutput.innerHTML = `<span class="text-secondary text-red">Error generating escalation: ${patient.escalation.error}</span>`;
    } else {
        escalationPanel.style.display = 'block'; // Show block but say no escalation
        if (actionButtons) actionButtons.style.display = 'none';
        ragOutput.innerHTML = `<span class="text-secondary">No current escalations for this patient.</span>`;
    }
    
    // Refresh Chart with new data
    initChart(patient);
}

async function submitDecision(decision) {
    if (!currentPatientId) return;
    
    try {
        const response = await fetch(`http://127.0.0.1:8000/alerts/${currentPatientId}/decision`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                decision: decision,
                clinician_id: 'DR-001' // Mock logged-in user
            })
        });
        
        const data = await response.json();
        if (response.ok) {
            alert(`Decision "${decision}" recorded successfully! The AI flow has resumed.`);
            document.getElementById('human-loop-actions').style.display = 'none';
            // Optionally clear the escalation data so it doesn't prompt again until a new crash
            if(patientsData[currentPatientId]) {
                delete patientsData[currentPatientId].escalation;
                populatePatientDetail(patientsData[currentPatientId]);
            }
        } else {
            alert(`Error: ${data.detail}`);
        }
    } catch (err) {
        console.error("Decision submission error:", err);
        alert("Failed to record decision.");
    }
}

// Chart initialization for the detailed view
let vitalsChartInstance = null;

let currentChartWindow = 60;

function setChartWindow(minutes, btnElement) {
    currentChartWindow = minutes;
    
    // Update active button state
    if (btnElement) {
        document.querySelectorAll('.chart-btn').forEach(b => b.classList.remove('active'));
        btnElement.classList.add('active');
    }
    
    const pid = document.getElementById('profile-id').innerText;
    if (pid && patientsData[pid]) {
        initChart(patientsData[pid]);
    }
}

function generateChartLabels(minutes) {
    const labels = [];
    for (let i = minutes; i >= 0; i--) {
        if (i % 5 === 0 || i === minutes || i === 0) {
            labels.push(`T-${i}m`);
        } else {
            labels.push('');
        }
    }
    return labels;
}

function initChart(patient) {
    const ctx = document.getElementById('vitalsChart');
    if (!ctx) return;
    
    // Destroy previous instance if it exists
    if (vitalsChartInstance) {
        vitalsChartInstance.destroy();
    }

    // Determine data window (slice the end of the arrays)
    const hrSlice = patient.hrData.slice(-currentChartWindow);
    const spo2Slice = patient.spo2Data.slice(-currentChartWindow);
    const bpSlice = patient.bpData.slice(-currentChartWindow);
    
    // Generate relative time labels
    const labels = generateChartLabels(currentChartWindow - 1);
    
    vitalsChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Heart rate',
                    data: hrSlice,
                    borderColor: '#10b981', // green
                    backgroundColor: '#10b981',
                    tension: 0.4,
                    borderWidth: 2,
                    pointRadius: 1,
                },
                {
                    label: 'SpO2',
                    data: spo2Slice,
                    borderColor: '#0f766e', // teal
                    backgroundColor: '#0f766e',
                    tension: 0.4,
                    borderWidth: 2,
                    pointRadius: 1,
                },
                {
                    label: 'Blood pressure',
                    data: bpSlice,
                    borderColor: '#3b82f6', // blue
                    backgroundColor: '#3b82f6',
                    tension: 0.4,
                    borderWidth: 2,
                    pointRadius: 1,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        boxWidth: 8
                    }
                }
            },
            scales: {
                y: {
                    min: 40,
                    max: 150,
                    grid: {
                        color: '#f1f5f9'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}
