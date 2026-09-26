---
protocol_id: PROT-RESP-01
category: respiratory
title: Respiratory Deterioration Protocol
source: Educational Prototype Guidelines (adapted from NEWS2 respiratory domain, GINA asthma guidelines, GOLD COPD guidelines)
severity_levels: [watch, warning, critical]
primary_vitals: [spo2, respiratory_rate]
supporting_signals: [oxygen_flow_rate, mental_status, work_of_breathing, peak_flow]
trend_window_minutes: 15
min_consecutive_readings: 3
retrieval_keywords: [respiratory failure, hypoxia, SpO2 drop, tachypnea, bradypnea, oxygen therapy, HFNC, BiPAP, intubation, accessory muscle use, asthma, COPD, pneumonia, pulmonary embolism, ARDS, pneumothorax]
diseases_covered: [asthma_exacerbation, copd_exacerbation, pneumonia, pulmonary_embolism, ards, tension_pneumothorax]
---

# Respiratory Deterioration Protocol

## Condition Definition (General Trigger)
A **concurrent** drop in SpO2 and rise (or abnormal fall) in Respiratory Rate (RR), sustained over at least
**3 consecutive readings within a 15-minute window**:

- SpO2 < 92% on room air (or < 88% for patients with documented COPD/baseline hypoxemia — use static
  context to select the correct threshold), **or** a drop of ≥ 3% from patient's charted baseline
- RR ≥ 24 breaths/min (tachypnea) **or** RR ≤ 8 breaths/min (bradypnea — often a pre-arrest sign)
- Increasing supplemental oxygen requirement to maintain the same SpO2 counts as a trend signal even if SpO2 is currently stable

A brief SpO2 dip that self-corrects within one reading should be treated as **noise** unless RR is also trending abnormal.

## Scoring Reference (NEWS2 Respiratory Sub-Score, adapted)
| Parameter | 3 pts | 2 pts | 1 pt | 0 pts | 1 pt | 2 pts | 3 pts |
|---|---|---|---|---|---|---|---|
| RR (/min) | ≤ 8 | — | 9–11 | 12–20 | — | 21–24 | ≥ 25 |
| SpO2 (%) | ≤ 91 | 92–93 | 94–95 | ≥ 96 | — | — | — |
| Supplemental O2 | — | Yes | — | No | — | — | — |

A respiratory sub-score ≥ 5, or any single parameter at 3 points, warrants urgent review regardless of total score.

## Disease-Specific Differential (use patient static context — history/diagnosis field — to select the right sub-profile)

### Asthma Exacerbation
- **History flag**: `history` includes "asthma"
- **Vital signature**: RR ≥ 25–30/min, SpO2 may stay near-normal early (compensated) then fall sharply late (a *falling* RR with worsening SpO2/silent chest is a critical, not reassuring, sign), HR often > 120 bpm from bronchodilator use and hypoxia, pulsus paradoxus may be present.
- **Adjusted thresholds**: Do not wait for SpO2 < 92% alone — in known asthmatics, RR ≥ 25 with audible wheeze/accessory muscle use or inability to speak in full sentences is Warning-tier even if SpO2 is still ≥ 92%. A drop in RR *with* falling SpO2 or new silent chest = Critical (impending respiratory arrest).
- **Distinguishing features**: Wheeze, prolonged expiration, history of recent inhaler/steroid use, peak flow < 50% of personal best if available.
- **Action additions**: Administer/escalate bronchodilators (short-acting beta-agonist) and systemic corticosteroids per physician order in addition to standard oxygen therapy; consider magnesium sulfate or escalation to ICU for severe/refractory cases.

### COPD Exacerbation
- **History flag**: `history` includes "COPD"
- **Vital signature**: Baseline SpO2 may run 88–92% chronically — use **patient-specific baseline**, not the general 92% cutoff, to judge deterioration. RR increase with prolonged expiration; may show CO2 retention signs (drowsiness, headache, flapping tremor) rather than just low SpO2.
- **Adjusted thresholds**: Target SpO2 88–92% (not > 92–96%) to avoid suppressing hypoxic respiratory drive; escalate on a drop of ≥ 3% from *their own* charted baseline rather than the general threshold, and on new/worsening confusion or drowsiness (possible CO2 narcosis) regardless of SpO2 value.
- **Distinguishing features**: Increased sputum volume/purulence, barrel chest history, long-term home O2 use noted in static context.
- **Action additions**: Controlled oxygen titration (avoid over-oxygenation), consider nebulized bronchodilators and steroids, check for CO2 retention if drowsiness develops (arterial/venous blood gas if available).

### Pneumonia
- **Vital signature**: Fever (correlate with sepsis protocol), RR ≥ 22, SpO2 declining gradually over hours, HR mildly elevated; often overlaps with sepsis criteria if systemic.
- **Distinguishing features**: New/worsening cough, purulent sputum, localized crackles, recent WBC elevation.
- **Cross-reference**: If HR/BP/temperature also trend abnormal, cross-check against the Sepsis Protocol — pneumonia is a common sepsis source.
- **Action additions**: Obtain sputum culture and chest imaging if not already done; treat per sepsis bundle if systemic criteria also met.

### Pulmonary Embolism (PE)
- **Vital signature**: Sudden-onset (not gradual) tachypnea and SpO2 drop, often with concurrent tachycardia (HR > 100) and normal or low blood pressure; classic triad of dyspnea, chest pain, tachycardia.
- **Distinguishing features**: Sudden onset (minutes, not hours), recent immobility/surgery/known clotting risk in static context, pleuritic chest pain, unilateral leg swelling history.
- **Adjusted thresholds**: Sudden-onset abnormal RR + SpO2 + tachycardia together, even without fever, should raise PE suspicion — treat as Critical tier given risk of rapid hemodynamic collapse.
- **Action additions**: Urgent imaging (CT pulmonary angiogram) per physician; anticoagulation consideration; monitor for hemodynamic collapse (massive PE = obstructive shock).

### Acute Respiratory Distress Syndrome (ARDS)
- **History flag**: recent sepsis, trauma, aspiration, or major surgery in static context.
- **Vital signature**: Progressive, refractory hypoxemia (SpO2 falling despite escalating O2 support) with bilateral pattern; RR climbing steadily.
- **Distinguishing features**: Onset within ~1 week of a known clinical insult (sepsis, trauma, pancreatitis); hypoxemia disproportionate to O2 support given.
- **Action additions**: Escalate respiratory support early (HFNC/BiPAP/intubation with lung-protective ventilation per physician); avoid fluid overload.

### Tension Pneumothorax
- **Vital signature**: Sudden severe SpO2 drop and tachypnea **with** hypotension and tachycardia (obstructive shock pattern), often after trauma, line placement, or mechanical ventilation.
- **Distinguishing features**: Sudden onset, absent breath sounds on one side, tracheal deviation, distended neck veins — this is a medical emergency requiring immediate needle decompression, not just oxygen escalation.
- **Adjusted thresholds**: Any sudden concurrent SpO2 drop + tachycardia + hypotension in a post-procedural/trauma/ventilated patient = Critical, bypass normal 3-reading confirmation window given the acuity.

## Assessment (General)
- Evaluate airway patency and work of breathing (accessory muscle use, nasal flaring, tripod positioning).
- Check for cyanosis and altered mental status (hypoxia- or CO2-driven).
- Confirm SpO2 with an alternative pulse oximeter if signal quality is poor.
- Pull patient's diagnosis/history field (asthma, COPD, recent surgery, trauma, clotting risk) to select the correct disease-specific sub-profile above **before** applying generic thresholds.
- Review recent oxygen therapy changes to avoid duplicate low-tier alerts once escalation is already underway.

## Action Plan (General)
| Urgency | Action |
|---|---|
| Immediate | Elevate head of bed to optimize ventilation and reduce work of breathing |
| Immediate | Initiate/increase supplemental oxygen — target per disease-specific profile above (88–92% for COPD, >92% otherwise) |
| If no improvement | Escalate to HFNC, BiPAP, or intubation per physician assessment |
| Immediate | Notify attending physician or Rapid Response Team |
| Critical tier | Prepare emergency airway equipment; alert respiratory therapy/ICU team |

## Escalation / Explanation Guidance (for agentic output)
Cite: (1) SpO2/RR trend with timestamps, (2) which disease-specific profile was applied and why (history flag matched), (3) current O2 delivery method, (4) distinguishing features observed, (5) tier-matched recommended action from the matched disease sub-section.

## Non-Actionable / Suppression Guidance
- Suppress repeat "Watch" alerts once "Warning"/"Critical" is active for the same patient/category.
- Do not suppress based on generic cooldown if a disease-specific critical pattern (e.g., tension pneumothorax signature) is newly detected.
