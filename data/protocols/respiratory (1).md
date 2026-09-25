---
protocol_id: PROT-RESP-01
category: respiratory
title: Respiratory Deterioration Protocol
source: Educational Prototype Guidelines (adapted from NEWS2 respiratory domain, ROX index concepts)
severity_levels: [watch, warning, critical]
primary_vitals: [spo2, respiratory_rate]
supporting_signals: [oxygen_flow_rate, mental_status, work_of_breathing]
trend_window_minutes: 15
min_consecutive_readings: 3
retrieval_keywords: [respiratory failure, hypoxia, SpO2 drop, tachypnea, bradypnea, oxygen therapy, HFNC, BiPAP, intubation, accessory muscle use]
---

# Respiratory Deterioration Protocol

## Condition Definition
A **concurrent** drop in SpO2 and rise (or abnormal fall) in Respiratory Rate (RR), sustained over at least
**3 consecutive readings within a 15-minute window**:

- SpO2 < 92% on room air (or < 88% for patients with documented COPD/baseline hypoxemia — use static
  context to select the correct threshold), **or** a drop of ≥ 3% from patient's charted baseline
- RR ≥ 24 breaths/min (tachypnea) **or** RR ≤ 8 breaths/min (bradypnea — often a pre-arrest sign)
- Increasing supplemental oxygen requirement to maintain the same SpO2 (e.g., flow rate escalation) counts as a trend signal even if SpO2 itself is currently stable

A brief SpO2 dip (e.g., due to probe displacement or patient movement) that self-corrects within one
reading should be treated as **noise** unless RR is also trending abnormal.

## Scoring Reference (NEWS2 Respiratory Sub-Score, adapted)
| Parameter | 3 pts | 2 pts | 1 pt | 0 pts | 1 pt | 2 pts | 3 pts |
|---|---|---|---|---|---|---|---|
| RR (/min) | ≤ 8 | — | 9–11 | 12–20 | — | 21–24 | ≥ 25 |
| SpO2 (%) | ≤ 91 | 92–93 | 94–95 | ≥ 96 | — | — | — |
| Supplemental O2 | — | Yes | — | No | — | — | — |

Sum contributes to overall early-warning score; a respiratory sub-score ≥ 5, or any single parameter at 3 points, warrants urgent review regardless of total score.

## Severity Tiering
- **Watch**: One parameter trending abnormal, not yet sustained 3 readings, or O2 requirement inching up.
- **Warning**: SpO2 < 92% or RR ≥ 24 (or ≤ 8), sustained, with stable mental status.
- **Critical**: SpO2 < 88% **and** RR abnormal, or any altered mental status / cyanosis / accessory muscle use present → treat as impending respiratory failure.

## Assessment
- Evaluate airway patency and work of breathing (accessory muscle use, nasal flaring, tripod positioning).
- Check for cyanosis (central vs peripheral) and altered mental status (hypoxia-driven confusion/agitation).
- Confirm SpO2 with an alternative pulse oximeter or waveform check if signal quality is poor before escalating on that reading alone.
- Review recent oxygen therapy changes and whether escalation has already begun (avoid duplicate low-tier alerts once a higher-tier intervention is already in progress).
- Correlate with static context: pre-existing lung disease, recent extubation, opioid administration (risk of hypoventilation/bradypnea).

## Action Plan
| Urgency | Action |
|---|---|
| Immediate | Elevate head of bed to optimize ventilation and reduce work of breathing |
| Immediate | Initiate/increase supplemental oxygen (nasal cannula → simple face mask → non-rebreather) targeting SpO2 > 92% (or patient's documented baseline) |
| If no improvement | Prepare for advanced respiratory support: High-Flow Nasal Cannula (HFNC), BiPAP, or intubation per physician assessment |
| Immediate | Notify attending physician or Rapid Response Team |
| Critical tier | Prepare emergency airway equipment and alert respiratory therapy/ICU team |

## Escalation / Explanation Guidance (for agentic output)
Cite: (1) SpO2 and RR trend values with timestamps, (2) whether the drop is sustained vs. transient, (3) current O2 delivery method/flow rate, (4) relevant static context (COPD, recent extubation, sedation), (5) the recommended tier-matched action.

## Non-Actionable / Suppression Guidance
- Suppress repeat "Watch" alerts once a "Warning" or "Critical" alert is active for the same patient.
- If a single desaturation is corrected by a documented probe re-placement/recalibration event, do not escalate on that reading.
