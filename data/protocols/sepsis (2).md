---
protocol_id: PROT-SEPSIS-01
category: sepsis_infectious_metabolic
title: Sepsis, Infectious & Metabolic Deterioration Protocol
source: Educational Prototype Guidelines (adapted from Sepsis-3, qSOFA, SIRS, Surviving Sepsis Campaign, ADA/DKA guidelines, WAO anaphylaxis criteria)
severity_levels: [watch, warning, critical]
primary_vitals: [heart_rate, respiratory_rate, blood_pressure_systolic, temperature]
supporting_signals: [wbc, lactate, mental_status, urine_output, blood_glucose, skin_findings]
trend_window_minutes: 30
min_consecutive_readings: 3
retrieval_keywords: [sepsis, infection, qSOFA, SIRS, septic shock, lactate, hypotension, fever, antibiotics, blood cultures, fluid resuscitation, urosepsis, anaphylaxis, DKA, diabetic ketoacidosis, hypovolemic shock, dehydration]
diseases_covered: [sepsis, septic_shock, urosepsis, anaphylaxis, diabetic_ketoacidosis, hypovolemic_shock]
---

# Sepsis, Infectious & Metabolic Deterioration Protocol

## Condition Definition (General Trigger)
Suspected or confirmed infection **plus** a sustained, concurrent change in two or more of the following
core vitals, persisting across at least **3 consecutive readings within a 30-minute window**:

- Heart Rate (HR) > 90 bpm, or a sustained rise of ≥ 20 bpm from baseline
- Respiratory Rate (RR) ≥ 22 breaths/min
- Systolic Blood Pressure (SBP) ≤ 100 mmHg, or a drop of ≥ 40 mmHg from baseline
- Temperature < 36.0 °C or > 38.3 °C
- New or worsening altered mental status

A single abnormal reading that reverts on the next sample is **noise**, not a trigger.

## Scoring Frameworks
### qSOFA (score ≥ 2 suggests high risk)
| Criterion | Points |
|---|---|
| RR ≥ 22/min | 1 |
| SBP ≤ 100 mmHg | 1 |
| Altered mentation (GCS < 15) | 1 |

### SIRS Criteria (≥ 2 met suggests systemic inflammatory response)
| Criterion | Threshold |
|---|---|
| Temperature | < 36.0 °C or > 38.0 °C |
| Heart rate | > 90 bpm |
| Respiratory rate | > 20/min |
| WBC | < 4,000/mm³ or > 12,000/mm³, or > 10% bands |

## Disease-Specific Differential

### Sepsis (general)
- **Vital signature**: ≥ 2 SIRS criteria + suspected infection source (any site).
- **Severity**: Watch = qSOFA 1; Warning = qSOFA 2 or SIRS ≥ 2 with source; Critical = qSOFA ≥ 2 with SBP ≤ 90 or lactate ≥ 4 mmol/L (septic shock).
- **Action**: See general Action Plan (Sepsis Six bundle) below.

### Septic Shock
- **Vital signature**: Sepsis criteria **plus** persistent hypotension (SBP ≤ 90 mmHg or MAP < 65 mmHg) despite 30 mL/kg fluid bolus, or lactate ≥ 4 mmol/L.
- **Distinguishing features**: Vasopressor requirement to maintain MAP ≥ 65 mmHg; skin mottling; oliguria (urine output < 0.5 mL/kg/hr).
- **Action additions**: Escalate to ICU-level care; initiate vasopressor support (e.g., norepinephrine) per physician order; recheck lactate every 2–4 hours.

### Urosepsis
- **History flag**: `history` includes UTI, catheter use, recent urologic procedure, or known urinary retention.
- **Vital signature**: Fever/rigors, tachycardia, flank pain if reported, may progress rapidly to hypotension in elderly patients.
- **Distinguishing features**: Positive urinalysis/culture, suprapubic or flank tenderness, cloudy/foul-smelling urine noted in nursing notes.
- **Adjusted thresholds**: In elderly or catheterized patients, altered mental status **without** fever can still indicate urosepsis — do not require fever as a mandatory criterion in this population.
- **Action additions**: Obtain urine culture in addition to blood cultures; consider catheter removal/exchange if indicated.

### Anaphylaxis
- **Trigger context**: Recent medication administration, new food exposure, insect sting, or contrast administration in the preceding minutes.
- **Vital signature**: Sudden-onset hypotension **and/or** respiratory distress (wheeze, stridor, SpO2 drop) **and** tachycardia, developing over minutes, often with skin findings (hives, flushing, angioedema).
- **Distinguishing features**: Rapid onset (minutes, not hours), temporal link to an exposure, skin/mucosal involvement, GI symptoms (vomiting, cramping).
- **Adjusted thresholds**: Bypass the standard 3-reading confirmation window — sudden concurrent hypotension + respiratory symptoms + recent exposure is Critical immediately given risk of airway compromise and cardiovascular collapse within minutes.
- **Action additions**: Administer intramuscular epinephrine immediately per protocol/physician order; secure airway; IV fluids for hypotension; H1/H2 blockers and corticosteroids as adjuncts; observe for biphasic reaction.

### Diabetic Ketoacidosis (DKA)
- **History flag**: `history` includes diabetes (especially Type 1); recent illness, missed insulin doses, or blood glucose readings available in supporting signals.
- **Vital signature**: Tachycardia and tachypnea (compensatory, deep/rapid "Kussmaul" breathing pattern), normal-to-low BP as dehydration progresses, blood glucose typically > 250 mg/dL.
- **Distinguishing features**: Fruity breath odor, nausea/vomiting, abdominal pain, polyuria/polydipsia history, altered mental status as it progresses.
- **Adjusted thresholds**: Tachypnea in DKA reflects respiratory *compensation* for metabolic acidosis, not primary lung pathology — do not treat with oxygen escalation alone; the priority is fluids/insulin/electrolyte correction.
- **Action additions**: Check point-of-care blood glucose and ketones immediately; initiate IV isotonic fluid resuscitation; notify physician for insulin therapy and potassium monitoring (insulin can precipitate dangerous hypokalemia).

### Hypovolemic Shock (Hemorrhage / Severe Dehydration)
- **History flag**: Recent trauma, GI bleed, surgery, or documented poor oral intake/vomiting/diarrhea.
- **Vital signature**: Progressive tachycardia followed by hypotension (compensated → decompensated shock), narrowing pulse pressure, delayed capillary refill, cool clammy skin.
- **Distinguishing features**: No fever (distinguishes from septic shock unless combined etiology); visible bleeding source or reported blood loss; orthostatic vital changes if measured.
- **Action additions**: Identify and control bleeding source if applicable; IV fluid/blood product resuscitation per physician; avoid mislabeling as sepsis if no infectious source is present.

## Assessment (General)
- Evaluate for signs of systemic infection vs. non-infectious causes (allergic exposure, glucose readings, bleeding/fluid loss history) using the disease differentials above.
- Review recent labs: WBC, lactate, blood glucose, ketones as applicable.
- Assess perfusion: capillary refill, skin mottling, temperature.
- Pull static context (diabetes, allergies, recent procedures, catheter use, anticoagulation) to select the correct disease sub-profile **before** applying generic sepsis thresholds.

## Action Plan (General Sepsis Bundle)
| Urgency | Action | Target Time |
|---|---|---|
| Immediate | Notify attending physician and Rapid Response Team | Immediately on Warning/Critical |
| Immediate | Obtain blood cultures before antibiotics (if infectious cause suspected) | Before antibiotics |
| Within 1 hr | Initiate empiric broad-spectrum IV antibiotics (infectious causes only) | ≤ 60 min |
| Within 1 hr | IV crystalloid fluid resuscitation, 30 mL/kg, for hypotension or lactate ≥ 4 mmol/L | ≤ 60 min |
| Ongoing | Draw/repeat serum lactate | Within 1 hr, repeat 2–4 hr |
| Ongoing | Continuous hemodynamic monitoring | Continuous |

## Escalation / Explanation Guidance (for agentic output)
Cite: (1) vitals crossed and duration, (2) qSOFA/SIRS components, (3) which disease-specific profile matched and the history flag that triggered it, (4) distinguishing features observed, (5) tier-matched recommended action.

## Non-Actionable / Suppression Guidance
- Do not re-fire the same tier within a cooldown window unless severity escalates.
- Anaphylaxis and severe DKA patterns bypass cooldown/suppression logic given rapid deterioration risk.
