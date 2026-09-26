---
protocol_id: PROT-CARDIO-01
category: cardiovascular
title: Cardiovascular Deterioration Protocol
source: Educational Prototype Guidelines (adapted from NEWS2 cardiovascular domain, ACC/AHA ACS & HF guidelines, ACLS)
severity_levels: [watch, warning, critical]
primary_vitals: [heart_rate, blood_pressure_systolic, blood_pressure_diastolic]
supporting_signals: [ecg_rhythm, mental_status, capillary_refill, spo2]
trend_window_minutes: 15
min_consecutive_readings: 3
retrieval_keywords: [tachycardia, bradycardia, hypotension, hypertensive crisis, arrhythmia, chest pain, cardiovascular instability, ECG, cardioversion, shock, myocardial infarction, heart failure, atrial fibrillation, cardiogenic shock, aortic dissection]
diseases_covered: [acute_coronary_syndrome, acute_decompensated_heart_failure, atrial_fibrillation_rvr, cardiogenic_shock, hypertensive_emergency, aortic_dissection, bradyarrhythmia_heart_block]
---

# Cardiovascular Deterioration Protocol

## Condition Definition (General Trigger)
Sudden changes in Heart Rate (HR) combined with hypotension or hypertension, sustained over at least
**3 consecutive readings within a 15-minute window**:

- Tachycardia: HR > 130 bpm, or a sustained rise ≥ 20 bpm from baseline
- Bradycardia: HR < 50 bpm, or a sustained drop ≥ 20 bpm from baseline
- Hypotension: SBP < 90 mmHg, or a drop ≥ 40 mmHg from baseline
- Hypertensive crisis: SBP > 180 mmHg or DBP > 120 mmHg
- New irregular rhythm reported by monitor counts as a corroborating signal

## Scoring Reference (NEWS2 Cardiovascular Sub-Score, adapted)
| Parameter | 3 pts | 2 pts | 1 pt | 0 pts | 1 pt | 2 pts | 3 pts |
|---|---|---|---|---|---|---|---|
| HR (bpm) | ≤ 40 | — | 41–50 | 51–90 | 91–110 | 111–130 | ≥ 131 |
| SBP (mmHg) | ≤ 90 | 91–100 | 101–110 | 111–219 | — | — | ≥ 220 |

## Disease-Specific Differential

### Acute Coronary Syndrome (ACS / Myocardial Infarction)
- **Vital signature**: Variable — may show tachycardia or bradycardia (if inferior MI with vagal effects), mild hypotension if cardiac output falls, or normal vitals early on. Vitals alone are often insufficient — rely heavily on reported symptoms.
- **Distinguishing features**: Chest pain/pressure, radiation to arm/jaw, diaphoresis, nausea, new ECG changes (ST elevation/depression); history of prior MI, diabetes, smoking, hyperlipidemia in static context increases pre-test probability.
- **Adjusted thresholds**: Treat any new chest pain report combined with even mild vital sign change (HR or BP trending abnormal) as Warning-tier minimum, regardless of absolute threshold — ACS can present with near-normal vitals.
- **Action additions**: Obtain 12-lead ECG within 10 minutes; aspirin per protocol/physician order; troponin labs; continuous cardiac monitoring; urgent cardiology notification.

### Acute Decompensated Heart Failure (ADHF)
- **History flag**: `history` includes heart failure/cardiomyopathy.
- **Vital signature**: Tachycardia, rising RR and falling SpO2 (pulmonary edema overlap with respiratory protocol), BP may be elevated (hypertensive HF) or low (cardiogenic, poor prognosis).
- **Distinguishing features**: Worsening dyspnea/orthopnea, weight gain, peripheral edema, crackles on exam, recent medication non-adherence (diuretics) noted in history.
- **Action additions**: Diuretic therapy per physician; oxygen support; fluid restriction; monitor strict intake/output; cross-reference respiratory protocol if SpO2/RR also trending.

### Atrial Fibrillation with Rapid Ventricular Response (AFib RVR)
- **Vital signature**: Irregularly irregular HR, typically > 110–150 bpm, may be associated with mild hypotension if rate is very high and filling time is compromised.
- **Distinguishing features**: Irregular rhythm on monitor/ECG (not just fast — irregular), palpitations reported, known AFib history or new onset.
- **Action additions**: 12-lead ECG to confirm rhythm; rate control (beta-blocker/calcium channel blocker) or rhythm control per physician; assess for anticoagulation status/stroke risk (cross-reference neurological protocol if any focal deficits appear — embolic stroke risk).

### Cardiogenic Shock
- **Vital signature**: Hypotension (SBP < 90 mmHg) **with** tachycardia, poor perfusion (cool extremities, delayed cap refill > 3 sec), low urine output, often in the setting of known MI/HF.
- **Distinguishing features**: Signs of end-organ hypoperfusion (altered mental status, oliguria) without an infectious or hemorrhagic source — distinguishes from septic/hypovolemic shock.
- **Action additions**: Urgent cardiology/ICU involvement; inotropic/vasopressor support per physician; avoid excessive fluids if pulmonary edema present (unlike hypovolemic shock management).

### Hypertensive Emergency
- **Vital signature**: SBP > 180 mmHg or DBP > 120 mmHg **with** evidence of acute end-organ damage (altered mental status, chest pain, visual changes, worsening renal function) — distinguishes from asymptomatic hypertensive urgency.
- **Distinguishing features**: Headache, visual disturbances, chest pain, focal neuro deficits (cross-reference neurological protocol).
- **Action additions**: Controlled, gradual BP reduction per physician order (rapid drops can cause ischemia); do not treat based on BP number alone without symptom correlation.

### Aortic Dissection
- **Vital signature**: Sudden severe hypertension or unequal BP readings between limbs (if measured), tachycardia, sudden-onset severe pain (tearing/ripping quality) reported.
- **Distinguishing features**: Sudden onset (not gradual), pain radiating to back, pulse deficits, history of hypertension/connective tissue disorder in static context.
- **Adjusted thresholds**: Sudden severe hypertension with reported tearing chest/back pain should bypass standard confirmation windows — treat as Critical immediately given rupture risk.
- **Action additions**: Urgent imaging (CT angiogram); strict BP and heart rate control per physician (beta-blockade first); emergency surgical consultation.

### Bradyarrhythmia / Heart Block
- **Vital signature**: HR < 50 bpm sustained, may be asymptomatic or associated with hypotension, dizziness, syncope.
- **Distinguishing features**: History of conduction disease, beta-blocker/calcium channel blocker/digoxin use in medication list (check for toxicity), recent cardiac procedure.
- **Action additions**: 12-lead ECG to characterize block type; hold AV-nodal blocking medications pending physician review; prepare for atropine or transcutaneous pacing if symptomatic/unstable.

## Assessment (General)
- Assess peripheral perfusion, capillary refill, pulse quality.
- Evaluate for chest pain, dizziness, palpitations, dyspnea, altered mental status.
- Obtain 12-lead ECG to characterize rhythm.
- Pull static context (cardiac history, medications, prior MI/HF/AFib) to select the correct disease sub-profile before applying generic thresholds.

## Action Plan (General)
| Urgency | Action |
|---|---|
| Immediate | Ensure patent IV access |
| If hypotensive | Consider positioning, prepare for physician-directed fluids (unless cardiogenic — see above) |
| If tachycardic/unstable | Prepare for cardioversion per ACLS |
| If hypertensive crisis | Notify physician for controlled antihypertensive management |
| Immediate | Notify attending physician or Rapid Response Team |

## Escalation / Explanation Guidance (for agentic output)
Cite: (1) HR/BP trend with timestamps, (2) cardiovascular sub-score, (3) which disease profile matched and supporting history/symptom flags, (4) ECG rhythm if available, (5) tier-matched recommended action.

## Non-Actionable / Suppression Guidance
- Standard cooldown applies for stable trending alerts; aortic dissection and cardiogenic shock patterns bypass cooldown/suppression given acuity.
