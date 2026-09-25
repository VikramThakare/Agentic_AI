---
protocol_id: PROT-CARDIO-01
category: cardiovascular
title: Cardiovascular Deterioration Protocol
source: Educational Prototype Guidelines (adapted from NEWS2 cardiovascular domain, ACLS concepts)
severity_levels: [watch, warning, critical]
primary_vitals: [heart_rate, blood_pressure_systolic, blood_pressure_diastolic]
supporting_signals: [ecg_rhythm, mental_status, capillary_refill]
trend_window_minutes: 15
min_consecutive_readings: 3
retrieval_keywords: [tachycardia, bradycardia, hypotension, hypertensive crisis, arrhythmia, chest pain, cardiovascular instability, ECG, cardioversion, shock]
---

# Cardiovascular Deterioration Protocol

## Condition Definition
Sudden changes in Heart Rate (HR) combined with hypotension or hypertension, sustained over at least
**3 consecutive readings within a 15-minute window**:

- Tachycardia: HR > 130 bpm (or > 110 bpm sustained with symptoms), or a sustained rise ≥ 20 bpm from baseline
- Bradycardia: HR < 50 bpm (or < 60 bpm if symptomatic), or a sustained drop ≥ 20 bpm from baseline
- Hypotension: SBP < 90 mmHg, or a drop ≥ 40 mmHg from baseline
- Hypertensive crisis: SBP > 180 mmHg or DBP > 120 mmHg, especially with symptoms (headache, chest pain, visual changes)
- New irregular rhythm reported by monitor (e.g., suspected atrial fibrillation, ventricular ectopy) counts as a corroborating signal even if rate is within normal range

Isolated single-reading artifacts (e.g., due to lead/cuff motion) that self-correct on the next sample
should be treated as **noise** unless a second parameter (BP, perfusion, symptoms) also trends abnormal.

## Scoring Reference (NEWS2 Cardiovascular Sub-Score, adapted)
| Parameter | 3 pts | 2 pts | 1 pt | 0 pts | 1 pt | 2 pts | 3 pts |
|---|---|---|---|---|---|---|---|
| HR (bpm) | ≤ 40 | — | 41–50 | 51–90 | 91–110 | 111–130 | ≥ 131 |
| SBP (mmHg) | ≤ 90 | 91–100 | 101–110 | 111–219 | — | — | ≥ 220 |

A cardiovascular sub-score ≥ 5, or any single parameter at 3 points, warrants urgent review regardless of total score.

## Severity Tiering
- **Watch**: One parameter trending abnormal, not yet sustained 3 readings, no symptoms reported.
- **Warning**: HR and BP both trending abnormal together, sustained, patient stable/asymptomatic.
- **Critical**: Hemodynamic instability with symptoms (chest pain, syncope, altered mental status) or SBP < 90 mmHg with tachycardia/bradycardia, or hypertensive crisis with symptoms.

## Assessment
- Assess peripheral perfusion: capillary refill time (> 3 sec abnormal), skin temperature and color, pulse quality.
- Evaluate the patient for chest pain, dizziness, palpitations, dyspnea, or altered mental status.
- Obtain an immediate 12-lead ECG to characterize rhythm (rate alone does not confirm arrhythmia type).
- Review static context: known arrhythmia history, cardiac medications (beta-blockers, antiarrhythmics), recent cardiac procedures, baseline BP/HR.

## Action Plan
| Urgency | Action |
|---|---|
| Immediate | Ensure patent IV access is available |
| If hypotensive | Consider laying patient flat/Trendelenburg if appropriate; prepare for physician-directed fluid resuscitation |
| If tachycardic and unstable | Prepare for immediate medical intervention or synchronized cardioversion per ACLS protocol |
| If hypertensive crisis with symptoms | Notify physician for urgent antihypertensive management; avoid precipitous BP drops |
| Immediate | Notify attending physician or Rapid Response Team immediately |
| Ongoing | Obtain/repeat 12-lead ECG; continuous cardiac and BP monitoring |

## Escalation / Explanation Guidance (for agentic output)
Cite: (1) HR and BP trend values with timestamps and direction, (2) computed cardiovascular sub-score, (3) presence/absence of symptoms and perfusion findings, (4) ECG rhythm if available, (5) relevant static context (cardiac history, current medications), (6) tier-matched recommended action.

## Non-Actionable / Suppression Guidance
- Do not re-fire the same tier alert within a short cooldown (e.g., 10–15 minutes) unless the patient escalates to the next severity tier or a new symptom appears.
- If HR/BP normalize for 2+ consecutive readings, downgrade the alert rather than continuing to display it as active.
