---
protocol_id: PROT-SEPSIS-01
category: sepsis
title: Sepsis Deterioration Protocol
source: Educational Prototype Guidelines (adapted from Sepsis-3, qSOFA, SIRS, Surviving Sepsis Campaign)
severity_levels: [watch, warning, critical]
primary_vitals: [heart_rate, respiratory_rate, blood_pressure_systolic, temperature]
supporting_signals: [wbc, lactate, mental_status, urine_output]
trend_window_minutes: 30
min_consecutive_readings: 3
retrieval_keywords: [sepsis, infection, qSOFA, SIRS, septic shock, lactate, hypotension, fever, antibiotics, blood cultures, fluid resuscitation]
---

# Sepsis Deterioration Protocol

## Condition Definition
Suspected or confirmed infection **plus** a sustained, concurrent change in two or more of the following
core vitals, persisting across at least **3 consecutive readings within a 30-minute window** (not a single
transient spike):

- Heart Rate (HR) > 90 bpm (adult) or a sustained rise of ≥ 20 bpm from patient baseline
- Respiratory Rate (RR) ≥ 22 breaths/min
- Systolic Blood Pressure (SBP) ≤ 100 mmHg, or a drop of ≥ 40 mmHg from baseline
- Temperature < 36.0 °C or > 38.3 °C
- New or worsening altered mental status (drop in GCS, confusion, lethargy)

A single abnormal reading that reverts on the next sample should be treated as **noise**, not a trigger.
Trend detection logic should weight the *direction and persistence* of change over the raw threshold
crossing (e.g., HR climbing 78 → 92 → 101 → 108 over 20 minutes is a stronger signal than one isolated
HR of 92).

## Scoring Frameworks (use for risk stratification, not sole trigger)

### qSOFA (quick Sequential Organ Failure Assessment) — score ≥ 2 suggests high risk
| Criterion | Points |
|---|---|
| Respiratory rate ≥ 22/min | 1 |
| Systolic BP ≤ 100 mmHg | 1 |
| Altered mentation (GCS < 15) | 1 |

### SIRS Criteria — ≥ 2 met suggests systemic inflammatory response
| Criterion | Threshold |
|---|---|
| Temperature | < 36.0 °C or > 38.0 °C |
| Heart rate | > 90 bpm |
| Respiratory rate | > 20/min or PaCO2 < 32 mmHg |
| WBC | < 4,000/mm³ or > 12,000/mm³, or > 10% bands |

### Severity Tiering for Escalation
- **Watch**: qSOFA = 1, or one core vital trending abnormal but not yet sustained 3 readings.
- **Warning**: qSOFA = 2 OR SIRS ≥ 2 with confirmed/suspected infection source.
- **Critical**: qSOFA ≥ 2 **and** SBP ≤ 90 mmHg or lactate ≥ 4 mmol/L → treat as **septic shock** until proven otherwise.

## Assessment
- Evaluate for signs of systemic infection (fever, chills, altered mental status, localized infection source).
- Review recent labs for elevated WBC (> 12,000/mm³) or elevated serum lactate (≥ 2 mmol/L abnormal, ≥ 4 mmol/L severe).
- Assess perfusion: capillary refill > 3 sec, skin mottling, cool extremities.
- Calculate qSOFA and/or SIRS using the tables above; use static per-patient context (age, comorbidities, baseline vitals) to adjust thresholds — e.g., a baseline tachycardic patient needs a delta-based rather than absolute HR threshold.
- Cross-check trend against recent medication administration (e.g., antipyretics, vasopressors) that could mask or mimic deterioration.

## Action Plan (Time-Critical — "Sepsis Six" style bundle)
| Urgency | Action | Target Time |
|---|---|---|
| Immediate | Notify attending physician and Rapid Response Team | Immediately on Warning/Critical tier |
| Immediate | Obtain blood cultures (2 sets) and other relevant cultures **before** antibiotics | Before antibiotic administration |
| Within 1 hr | Initiate empiric broad-spectrum IV antibiotics | ≤ 60 minutes from recognition |
| Within 1 hr | Administer IV crystalloid fluid resuscitation, 30 mL/kg, for hypotension or lactate ≥ 4 mmol/L | ≤ 60 minutes (reassess for fluid overload risk in cardiac/renal patients) |
| Ongoing | Draw serum lactate; repeat if initial value elevated | Within 1 hr, repeat at 2–4 hr |
| Ongoing | Continuous hemodynamic monitoring (HR, BP, SpO2, urine output) | Continuous |
| If refractory | Escalate for vasopressor support (e.g., norepinephrine) if hypotension persists after fluids | Per physician order |

## Escalation / Explanation Guidance (for agentic output)
When generating a clinician-facing escalation, the explanation should cite:
1. Which specific vitals crossed threshold and for how long (trend evidence).
2. The computed qSOFA/SIRS score and its components.
3. Relevant static context (e.g., recent surgery, immunosuppression, known infection source).
4. The recommended next action from the table above, tied to the severity tier.

## Non-Actionable / Suppression Guidance
- Do not re-fire the same alert tier for the same patient within a cooldown window (e.g., 15–20 minutes) unless severity escalates to the next tier.
- A single vital returning to baseline for 2+ consecutive readings should downgrade or clear the alert rather than continuing to fire.
