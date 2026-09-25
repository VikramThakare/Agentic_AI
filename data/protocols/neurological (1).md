---
protocol_id: PROT-NEURO-01
category: neurological
title: Neurological Deterioration Protocol
source: Educational Prototype Guidelines (adapted from Cushing's Triad, GCS, FAST stroke screen)
severity_levels: [watch, warning, critical]
primary_vitals: [heart_rate, blood_pressure, respiratory_pattern]
supporting_signals: [gcs, pupil_reactivity, blood_glucose]
trend_window_minutes: 20
min_consecutive_readings: 2
retrieval_keywords: [Cushing triad, increased intracranial pressure, ICP, stroke, FAST, GCS drop, bradycardia, widened pulse pressure, altered mental status, hypoglycemia]
---

# Neurological Deterioration Protocol

## Condition Definition
Sudden changes in vitals potentially linked to increased intracranial pressure (ICP) or acute
cerebrovascular event, flagged by **either** of the following patterns:

### Pattern A — Cushing's Triad (classic late sign of raised ICP; any 2 of 3 = high suspicion, all 3 = critical)
- Bradycardia: HR < 60 bpm, or a sustained drop of ≥ 20 bpm from baseline
- Irregular or abnormal respiratory pattern (e.g., Cheyne-Stokes, ataxic breathing)
- Widened pulse pressure: (SBP − DBP) increasing, typically with rising SBP and falling/steady DBP

### Pattern B — Sudden Altered Mental Status
- Drop in Glasgow Coma Scale (GCS) of ≥ 2 points from the last documented baseline, **or** any new GCS < 13
- New focal neurological deficit (facial droop, unilateral weakness, slurred speech) — map to FAST screen
- Sudden onset, within a 20-minute window (not a gradual sedation-related decline, which should be cross-checked against medication administration times)

A single abnormal HR or BP reading without a corroborating second signal (respiratory pattern change,
mental status change) should be treated as **watch-tier**, not an immediate critical trigger.

## Assessment
- Perform an immediate rapid neurological exam: GCS (eye/verbal/motor), pupil size and reactivity (unequal or non-reactive pupils are a red flag).
- Apply FAST screen: Face drooping, Arm weakness, Speech difficulty, Time of onset (critical for stroke treatment windows).
- Evaluate recent vitals for the HR-down/BP-up pattern characteristic of Cushing's triad.
- Check blood glucose immediately to rule out severe hypoglycemia (< 70 mg/dL) as a mimicking or contributing cause — this is a rapidly reversible cause of altered mental status and must be excluded early.
- Review static context: anticoagulant use, recent head trauma or neurosurgery, seizure history, baseline cognitive status.

## Severity Tiering
- **Watch**: One Cushing's-triad component present in isolation, or GCS drop of 1 point.
- **Warning**: Two Cushing's-triad components present, or GCS drop ≥ 2 points, or a positive FAST finding.
- **Critical**: All three Cushing's-triad components present, GCS < 8, or GCS drop ≥ 2 points with a positive FAST finding → treat as neurological emergency.

## Action Plan
| Urgency | Action |
|---|---|
| Immediate | Elevate head of bed to 30° to reduce ICP, if hemodynamically safe |
| Immediate | Maintain airway patency; prepare for intubation if GCS drops below 8 |
| Immediate | Notify attending physician and neurology/stroke team immediately |
| Immediate | Check point-of-care blood glucose to exclude hypoglycemia |
| Critical tier | Prepare patient for emergency CT head if stroke or hemorrhage is suspected |
| Ongoing | **Do not** administer hypotensive medications without specific physician orders — cerebral perfusion pressure must be maintained; lowering BP inappropriately in suspected raised-ICP states can worsen ischemia |

## Escalation / Explanation Guidance (for agentic output)
Cite: (1) which Cushing's-triad components are present and their values/trend, (2) GCS trajectory with timestamps, (3) FAST findings if any, (4) glucose result, (5) relevant static context (anticoagulation, prior neuro history), (6) tier-matched recommended action, explicitly noting the "do not administer hypotensives without orders" caution when BP is elevated in this context.

## Non-Actionable / Suppression Guidance
- Do not suppress or downgrade a Critical-tier neurological alert based on cooldown timers — neuro deterioration can progress rapidly and re-evaluation should remain frequent even after first notification, unless a clinician has explicitly dismissed/deferred it.
- Distinguish sedation-related GCS decline (check medication administration record) from spontaneous decline before escalating as a stroke/ICP event.
