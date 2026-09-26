---
protocol_id: PROT-NEURO-01
category: neurological
title: Neurological Deterioration Protocol
source: Educational Prototype Guidelines (adapted from Cushing's Triad, GCS, FAST/NIHSS stroke screens, status epilepticus guidelines)
severity_levels: [watch, warning, critical]
primary_vitals: [heart_rate, blood_pressure, respiratory_pattern]
supporting_signals: [gcs, pupil_reactivity, blood_glucose, temperature]
trend_window_minutes: 20
min_consecutive_readings: 2
retrieval_keywords: [Cushing triad, increased intracranial pressure, ICP, stroke, FAST, GCS drop, bradycardia, widened pulse pressure, altered mental status, hypoglycemia, seizure, status epilepticus, meningitis, encephalitis, traumatic brain injury]
diseases_covered: [ischemic_stroke, hemorrhagic_stroke, traumatic_brain_injury, status_epilepticus, meningitis_encephalitis, hypoglycemia]
---

# Neurological Deterioration Protocol

## Condition Definition (General Trigger)
Sudden changes in vitals potentially linked to increased intracranial pressure (ICP) or acute
cerebrovascular event:

### Pattern A — Cushing's Triad (any 2 of 3 = high suspicion, all 3 = critical)
- Bradycardia: HR < 60 bpm, or a sustained drop of ≥ 20 bpm from baseline
- Irregular/abnormal respiratory pattern
- Widened pulse pressure (rising SBP, falling/steady DBP)

### Pattern B — Sudden Altered Mental Status
- GCS drop of ≥ 2 points from baseline, or any new GCS < 13
- New focal deficit (facial droop, unilateral weakness, slurred speech)
- Sudden onset within a 20-minute window

## Disease-Specific Differential

### Ischemic Stroke
- **Vital signature**: Often normal or mildly elevated BP (permissive hypertension is physiologic, do not treat aggressively), HR usually normal unless comorbid arrhythmia (e.g., AFib as embolic source — cross-reference cardiovascular protocol).
- **Distinguishing features**: FAST-positive (face droop, arm weakness, speech difficulty), sudden onset, time-of-onset is critical for treatment eligibility window (note exact time last known well).
- **Adjusted thresholds**: A positive FAST/focal deficit finding is Warning-tier minimum even with otherwise normal vitals; escalate to Critical if GCS also dropping or symptoms worsening.
- **Action additions**: Note exact "last known well" time; urgent CT head (non-contrast) to rule out hemorrhage before any thrombolytic consideration; do not lower BP aggressively (permissive hypertension protects perfusion to ischemic penumbra) without physician/stroke-team order.

### Hemorrhagic Stroke
- **Vital signature**: Often presents with significant hypertension, possible Cushing's-triad component if ICP rising, rapid GCS decline more common than in ischemic stroke.
- **Distinguishing features**: Sudden severe headache ("worst headache of life"), vomiting, rapidly declining consciousness, anticoagulant use in history (major risk factor).
- **Adjusted thresholds**: Rapid GCS decline plus hypertension plus anticoagulant history should be treated as Critical immediately, bypassing standard confirmation window given bleed expansion risk.
- **Action additions**: Urgent CT head; reverse anticoagulation per physician if applicable; strict, physician-directed BP control (different targets than ischemic stroke — do not apply the same "permissive hypertension" rule here); neurosurgical consultation.

### Traumatic Brain Injury (TBI) / Raised ICP
- **History flag**: Recent head trauma, fall, or neurosurgical procedure in static context.
- **Vital signature**: Cushing's triad progression is the hallmark; GCS decline over time is more concerning than a single low value.
- **Distinguishing features**: Known trauma mechanism, pupil asymmetry/non-reactivity, vomiting, worsening headache.
- **Action additions**: Elevate head of bed 30°; maintain normotension/normoxia (avoid secondary injury from hypotension or hypoxia); urgent CT head; neurosurgical consultation; avoid hyperventilation unless herniation is imminent and physician-directed.

### Status Epilepticus / Seizure
- **Vital signature**: Tachycardia and hypertension during active seizure (sympathetic surge), followed by post-ictal hypotension/bradycardia and depressed GCS; SpO2 may drop during the event (airway compromise).
- **Distinguishing features**: Witnessed convulsive activity, or reported seizure history with sudden altered mental status and no clear alternative cause; seizure lasting > 5 minutes or recurrent seizures without return to baseline = status epilepticus (medical emergency).
- **Adjusted thresholds**: A seizure lasting > 5 minutes, or two or more seizures without full recovery between them, is Critical regardless of vital sign values.
- **Action additions**: Protect airway, position patient safely, time the seizure; benzodiazepine administration per protocol/physician for prolonged seizures; check glucose immediately (hypoglycemia can cause seizures); notify neurology.

### Meningitis / Encephalitis
- **Vital signature**: Fever (cross-reference sepsis protocol), tachycardia, may develop altered mental status and, in severe cases, Cushing's-triad signs if ICP rises.
- **Distinguishing features**: Neck stiffness, photophobia, headache, rash (in meningococcal disease), recent infection or immunosuppression in history.
- **Action additions**: Urgent lumbar puncture and blood cultures if not contraindicated; empiric antibiotics/antivirals per physician without delay; droplet precautions until meningococcal cause excluded.

### Hypoglycemia (Neurological Presentation)
- **Vital signature**: Sudden altered mental status/confusion/agitation, often with tachycardia and diaphoresis (adrenergic response); can mimic stroke or seizure.
- **Distinguishing features**: Blood glucose < 70 mg/dL confirmed on point-of-care testing; known diabetic on insulin/sulfonylurea in history; rapid, near-complete symptom resolution after glucose administration.
- **Adjusted thresholds**: Always check glucose **first**, before assuming stroke/ICP/seizure — this is the fastest reversible cause of acute altered mental status and must be excluded within minutes.
- **Action additions**: Administer oral or IV glucose per protocol immediately if confirmed; recheck GCS and glucose after treatment; investigate cause (missed meal, medication error) once stabilized.

## Assessment (General)
- Perform rapid neuro exam: GCS, pupil size/reactivity.
- Apply FAST/NIHSS screen for stroke.
- **Check blood glucose immediately** in any case of sudden altered mental status, before other workup.
- Pull static context (anticoagulants, seizure history, recent trauma/surgery, diabetes) to select the correct disease sub-profile.

## Action Plan (General)
| Urgency | Action |
|---|---|
| Immediate | Elevate head of bed to 30° if hemodynamically safe |
| Immediate | Maintain airway; prepare for intubation if GCS < 8 |
| Immediate | Notify attending physician and neurology/stroke team |
| Immediate | Check point-of-care glucose |
| Critical tier | Prepare for emergency CT head |
| Ongoing | Do not administer hypotensive medications without specific orders (except per disease-specific hemorrhagic stroke/dissection guidance above) |

## Escalation / Explanation Guidance (for agentic output)
Cite: (1) Cushing's-triad/GCS trend with timestamps, (2) FAST/seizure findings if any, (3) glucose result, (4) which disease profile matched and the history/symptom flag that triggered it, (5) tier-matched recommended action, including any "do not treat BP the same way" caveats.

## Non-Actionable / Suppression Guidance
- Do not suppress Critical-tier neuro alerts on cooldown timers — re-evaluate frequently until a clinician dismisses/defers.
- Status epilepticus and hemorrhagic-stroke patterns bypass standard confirmation windows given acuity.
