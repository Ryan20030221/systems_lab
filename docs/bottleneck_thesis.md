# Bottleneck Thesis

## Module

Module 12.25 — Bottleneck Thesis and Resource Taxonomy

## Artifact purpose

This document defines the project's current Layer 0 bottleneck thesis.

A bottleneck thesis is a structured, falsifiable working claim about what may limit throughput, efficiency, reliability, cost, or operational speed. It is not a final truth. It should guide future modules while remaining open to being disproven.

This document exists so future resource expansion is evidence-driven instead of random.

## Current thesis

AI infrastructure throughput-per-dollar is limited by interacting bottlenecks across compute, memory, storage, network, power, cooling, thermal behavior, scheduler decisions, human workflow, and heterogeneous device placement.

The current project should first build an observe → validate → diagnose → report → recommend foundation before attempting prediction, automation, or controller behavior.

The near-term product wedge remains load placement and avoidance: identify when a workload, pairing, placement, or resource condition is likely to produce poor performance, unsafe operation, wasted power, or unclear diagnosis.

## Current confidence

Overall thesis confidence: **low-to-medium**.

Reason:

- The project has real prior GPU experiment evidence around power, utilization, temperature, and performance.
- The project now has validation, reporting, and diagnosis foundations.
- The current evidence is still mostly single-GPU and does not yet prove cluster-level scheduler, network, storage, cooling, or heterogeneous-device bottlenecks.

The thesis is strong enough to guide the next learning/product direction, but not strong enough to justify autonomous control, production scheduling, or broad infrastructure claims.

## Scope boundary

This thesis currently supports:

- conservative diagnosis language
- resource taxonomy
- future evidence collection priorities
- future placement/avoidance reasoning
- future module selection

This thesis does **not** yet support:

- automatic production control
- claiming one universal bottleneck
- replacing a scheduler
- cluster-wide optimization claims
- safety-critical power or thermal automation
- high-confidence diagnosis without evidence

## Relationship to Module 12 diagnosis policy

Module 12 established that bottleneck claims must be evidence-based and conservative.

Future modules that make bottleneck, placement, scheduler, controller, thermal, power, or performance-explanation claims must reuse or audit:

```python
from gpu_lab.diagnosis import diagnose_experiments
```

and the policy documented in:

```text
docs/gpu_bottleneck_diagnosis_stack.md
```

This thesis inherits the same rules:

- symptoms are not automatically root causes
- competing explanations must be included
- confidence must be stated
- limitations must be stated
- `unknown` is an acceptable result
- `insufficient evidence` is an acceptable result
- claims should not exceed the evidence

---

# What the project currently knows

## Known with some evidence

### 1. Power and performance interact

Prior project experiments varied GPU power behavior and measured performance or efficiency outcomes. This supports the idea that power settings can matter for throughput-per-watt.

This does not prove that power is always the bottleneck.

### 2. GPU telemetry can support structured analysis

The project has already created reusable artifacts for parsing, validation, summaries, reporting, configuration, experiment-summary loading, and diagnosis.

This supports the idea that a structured observe → diagnose workflow is realistic.

### 3. Diagnosis needs conservative evidence handling

Module 12 established diagnosis outputs with evidence notes, confidence, competing explanations, limitation notes, `unknown`, and `insufficient evidence`.

This supports the idea that future placement or controller behavior must be explainable before it is trusted.

### 4. Human workflow is itself a bottleneck candidate

The project has repeatedly needed source-of-truth handoffs, contracts, docs, reusable artifacts, branch discipline, and checks. This supports the idea that operational clarity is part of the product foundation.

---

# What the project suspects

## Suspected thesis components

### 1. Placement will matter

The project suspects that poor placement, bad workload pairing, or missing resource awareness can reduce throughput or efficiency.

Current confidence: **low**.

Reason: the product wedge depends on placement, but current evidence does not yet include enough placement history or multi-job interference data.

### 2. Power and thermal behavior may affect future recommendations

The project suspects that power caps, temperature, and sustained load behavior may influence placement and workload decisions.

Current confidence: **low-to-medium**.

Reason: prior experiments include power, temperature, and performance, but more evidence is required before making strong claims.

### 3. Memory, storage, and network may become necessary expansion domains

The project suspects these resources will matter later, especially for larger or distributed workloads.

Current confidence: **low**.

Reason: these resources are common bottleneck candidates in systems work, but current project evidence does not yet measure them directly.

### 4. Heterogeneous device placement may matter later

The project suspects that matching workloads to device types may matter in mixed hardware environments.

Current confidence: **low**.

Reason: this is a likely long-term concern, but current evidence does not include multiple GPU classes or accelerator types.

---

# What the project does not know yet

The project does not yet know:

- whether target workloads are mostly compute-bound, memory-bound, communication-bound, storage-bound, power-bound, thermal-bound, or scheduler-bound
- whether bad placement happens often enough to be valuable to detect
- whether multi-job interference is common in the target environment
- whether power smoothing or thermal spreading produces meaningful throughput gains
- whether memory bandwidth or capacity is a dominant issue for target workloads
- whether network topology matters for the first real customer/user environment
- whether storage stalls explain low GPU utilization in real workloads
- whether heterogeneous device routing is needed soon or much later
- what minimum evidence is required before a recommendation should be trusted

These unknowns should drive future measurement and module design.

---

# Evidence supporting the thesis

## Supporting evidence 1 — Existing GPU experiment loop

The project has already gone through a loop of collecting GPU data, summarizing it, validating it, reporting it, and diagnosing possible bottlenecks.

This supports the thesis that structured evidence can guide future resource decisions.

## Supporting evidence 2 — Power/performance observations

Prior GPU experiments showed that performance, power, temperature, utilization, and efficiency can be measured together.

This supports the idea that resource tradeoffs can be made visible.

## Supporting evidence 3 — Reusable validation and diagnosis artifacts

The project now includes validation boundaries and reusable diagnosis logic.

This supports the idea that future claims can be grounded in structured inputs rather than manual guessing.

## Supporting evidence 4 — Product wedge alignment

The resource taxonomy and bottleneck thesis directly support the product wedge: load placement and avoidance.

Placement decisions need explanations, and explanations need resource-domain evidence.

---

# Evidence against or limiting the thesis

## Limitation 1 — Current evidence is mostly single-GPU

Single-GPU evidence does not prove cluster-level scheduling, networking, storage, cooling, or heterogeneous-device bottlenecks.

## Limitation 2 — Current evidence does not yet include enough workload diversity

A small set of experiments may not represent real production workloads.

## Limitation 3 — Some resource domains are not measured yet

Memory bandwidth, storage I/O, network traffic, placement history, queue time, fan behavior, and ambient conditions are not yet first-class evidence sources in the project.

## Limitation 4 — Product value is not proven yet

The project has a plausible wedge, but it still needs evidence that placement/avoidance recommendations produce meaningful improvements.

## Limitation 5 — Correlation is not root cause

Even when two metrics move together, the project must avoid treating correlation as proof of causation without more evidence.

---

# Disproof criteria

The thesis should be weakened or revised if repeated future evidence shows that:

1. workload performance is stable across placements,
2. colocated workloads do not interfere in meaningful ways,
3. power caps do not improve efficiency or safety under realistic workloads,
4. thermal behavior does not affect sustained performance,
5. memory, storage, and network measurements do not explain performance variance,
6. diagnosis outputs rarely produce useful explanations beyond obvious summaries,
7. users do not value placement/avoidance explanations,
8. simpler monitoring or reporting tools solve the problem well enough,
9. the cost of collecting evidence is higher than the value of the recommendation.

If several of these are true, the project should reconsider the placement-intelligence wedge or narrow the product scope.

---

# Expansion decision rules

Future expansion must be evidence-gated.

## Compute expansion

Expand compute-specific diagnosis when repeated experiments show high utilization, stable power/thermal behavior, and throughput limited after other causes are checked.

## Memory expansion

Expand memory logic when throughput or stability changes correlate with VRAM capacity, memory bandwidth, memory allocation pressure, or memory-heavy workload pairing.

## Storage expansion

Expand storage logic when GPU idle time, startup delay, checkpoint delay, or inconsistent runtime correlates with data loading or filesystem behavior.

## Network expansion

Expand network logic when distributed workloads show communication stalls, topology-sensitive performance, or GPU idle time during synchronization.

## Power expansion

Expand power logic when throughput, clock behavior, or efficiency changes predictably with power limits, or when placement decisions need to avoid power-budget conflicts.

## Cooling expansion

Expand cooling logic when sustained workloads show environment-level heat buildup, airflow problems, or temperature correlation across devices or locations.

## Thermal expansion

Expand thermal logic when repeated runs show temperature-correlated clock drops, throttle flags, or performance degradation over time.

## Scheduler expansion

Expand scheduler logic when placement history, queue time, or colocated workload data shows repeatable performance differences based on where or when jobs run.

## Human workflow expansion

Expand workflow tooling when manual experiment, diagnosis, reporting, or handoff work repeatedly slows progress or causes mistakes.

## Heterogeneous-device expansion

Expand heterogeneous-device logic when workloads show meaningful performance, cost, reliability, or memory differences across device classes.

---

# Current bottleneck ranking

This ranking is provisional and should be updated when new evidence arrives.

| Rank | Domain | Current status | Confidence | Reason |
|---|---|---|---|---|
| 1 | Human workflow | Active support bottleneck | Medium | The project repeatedly benefits from structure, checks, and reusable artifacts. |
| 2 | Power / thermal / compute interaction | Active evidence candidate | Low-to-medium | Prior GPU experiments measured these together, but root cause claims still require caution. |
| 3 | Scheduler / placement | Product wedge candidate | Low | Important to the business direction, but needs placement and interference evidence. |
| 4 | Memory | Deferred evidence candidate | Low | Plausible, but not measured deeply yet. |
| 5 | Storage | Deferred evidence candidate | Low | Plausible, but not measured yet. |
| 6 | Network | Deferred distributed-systems candidate | Low | Important later, but not proven by single-GPU evidence. |
| 7 | Cooling | Deferred infrastructure candidate | Low | Needs environment/rack-level data. |
| 8 | Heterogeneous device | Long-term candidate | Low | Needs multiple device classes or workload-device mismatch evidence. |

This ranking should not be read as universal truth. It is a current project planning tool.

---

# No-overclaiming rules

The project should avoid these claims unless future evidence supports them:

- "Power is the bottleneck."
- "The scheduler is bad."
- "This workload is compute-bound."
- "This placement is wrong."
- "Thermal throttling caused the slowdown."
- "Network is the reason scaling is poor."
- "The controller should automatically change the system."

Prefer conservative versions:

- "Power is a plausible contributing factor."
- "Scheduler placement may be relevant, but placement evidence is required."
- "The workload shows symptoms consistent with compute pressure."
- "This placement should be investigated because evidence suggests possible interference."
- "Thermal behavior may be relevant if temperature correlates with clock or performance changes."
- "Network evidence is required before diagnosing communication bottleneck."
- "A dry-run recommendation can be produced before any automated control action."

---

# Future reuse trigger

Audit or update this thesis whenever a future module:

- adds a new resource domain,
- changes diagnosis labels,
- creates placement recommendations,
- introduces controller decisions,
- adds telemetry sources,
- claims a performance root cause,
- expands into memory, storage, network, power, cooling, thermal, scheduler, or heterogeneous-device logic,
- changes the product wedge.

## Required update behavior

When new evidence arrives, update this document by changing one or more of:

- current thesis
- confidence
- supporting evidence
- evidence against
- unknowns
- disproof criteria
- expansion rules
- current bottleneck ranking

Do not only add supporting evidence. Add weakening evidence and unknowns when they exist.

---

# Docs-only review checklist

Before this document is considered complete, verify:

- [ ] The thesis is stated clearly.
- [ ] The thesis is falsifiable.
- [ ] Confidence is stated.
- [ ] Supporting evidence is included.
- [ ] Evidence against or limitations are included.
- [ ] Unknowns are included.
- [ ] Disproof criteria are included.
- [ ] Expansion decision rules are included.
- [ ] Current bottleneck ranking is marked provisional.
- [ ] Module 12 diagnosis policy is referenced.
- [ ] Future reuse trigger is included.
- [ ] The document does not claim production control readiness.
- [ ] The document does not claim a single universal bottleneck.
