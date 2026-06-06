# Resource Taxonomy

## Module

Module 12.25 — Bottleneck Thesis and Resource Taxonomy

## Artifact purpose

This document is the project's Layer 0 taxonomy for resources that can become bottlenecks in AI infrastructure and GPU systems work.

The goal is not to prove that every listed resource is currently a bottleneck. The goal is to define the resource domains, the symptoms they can produce, the evidence required to diagnose them, the software control levers that may exist, and the conditions that would justify future expansion.

Future bottleneck, placement, scheduler, controller, telemetry, thermal, power, or performance-explanation modules must audit this taxonomy before adding new resource-domain logic.

## Relationship to Module 12

Module 12 created the evidence-based diagnosis stack. This taxonomy follows that policy:

- do not claim a bottleneck from one weak metric alone
- separate symptoms from root causes
- include confidence
- include competing explanations
- include limitation notes
- allow `unknown` and `insufficient evidence`
- prefer conservative labels over overclaiming

Any future module that makes bottleneck claims should reuse or audit:

```python
from gpu_lab.diagnosis import diagnose_experiments
```

and the policy documented in:

```text
docs/gpu_bottleneck_diagnosis_stack.md
```

## Confidence scale

Use the same discipline as the diagnosis stack.

| Confidence | Meaning |
|---|---|
| Low | The resource is plausible, but evidence is incomplete or competing explanations remain. |
| Medium | Multiple signals support the resource as relevant, but some uncertainty remains. |
| High | Repeated evidence supports the resource and major competing explanations have been ruled out. |

Current default for most non-GPU domains is **low confidence** because the project has not yet collected broad multi-resource evidence.

## Expansion decision rule

A resource domain should only become a future implementation target when at least one of these is true:

1. repeated experiment evidence points to the domain,
2. diagnosis output repeatedly produces `unknown` because this domain is not measured,
3. placement decisions cannot be explained without this domain,
4. performance changes correlate with a measurement from this domain,
5. the product wedge needs this domain to avoid bad placement or explain poor performance.

If none of these are true, the domain remains documented but deferred.

---

# Resource domains

## Summary table

| Resource domain | What it means | Main symptom pattern | Software controllability | Current confidence |
|---|---|---|---|---|
| Compute | GPU/CPU execution capacity, clocks, utilization, instruction throughput | High utilization with throughput limited by execution capacity | Medium | Low-to-medium |
| Memory | VRAM/RAM capacity, bandwidth, allocation pressure, memory movement | Utilization stalls, OOM, bandwidth saturation, inconsistent throughput | Medium | Low |
| Storage | Disk/object-store read/write throughput and latency | GPU waits while data loads slowly | Medium | Low |
| Network | Host-to-host or device-to-device communication | Distributed jobs wait on communication instead of compute | Medium-to-high for placement, low for physical bandwidth | Low |
| Power | Electrical power budget, power caps, power throttling | Clocks/performance change around power limits | Medium | Low-to-medium |
| Cooling | Room, rack, airflow, fan, and heat-removal capacity | Many devices get hotter or throttle under sustained load | Low-to-medium | Low |
| Thermal | Device temperature and thermal throttling | Temperature rises, clocks drop, performance degrades | Medium | Low-to-medium |
| Scheduler | Job placement, queueing, co-location, resource assignment | Workloads interfere or wait despite available hardware | High | Low |
| Human workflow | Manual experiment, triage, reporting, and operational delay | Slow diagnosis, inconsistent reproduction, unclear decisions | High | Medium |
| Heterogeneous device | Choosing between GPU/CPU/other accelerators or different GPU types | Workload runs on a mismatched device | High for routing, low for hardware capability | Low |

---

## 1. Compute

### Definition

Compute means execution capacity: GPU SMs/cores, CPU cores, clock frequency, utilization, instruction throughput, and the ability of the hardware to perform useful work.

### Bottleneck symptoms

- GPU utilization stays high while throughput does not improve.
- Clock frequency is stable but performance is capped.
- More power or higher clocks produce only limited gains.
- A workload appears execution-heavy rather than data-transfer-heavy.

### Measurements that support this bottleneck

- sustained high GPU utilization
- stable clocks during the run
- stable temperature below thermal limits
- no obvious storage/network wait
- repeated runs showing throughput limited even when other resources appear healthy

### Measurements that weaken this bottleneck

- low or unstable GPU utilization
- large idle gaps
- storage, memory, network, power, or thermal symptoms
- performance improves mostly by fixing data movement instead of execution capacity

### Software controllability

Medium. Software usually cannot create more compute capacity, but it can change placement, workload pairing, batch size, precision, scheduling, power caps, and whether compute-heavy jobs are colocated.

### Current confidence

Low-to-medium.

Prior project experiments include GPU utilization and performance measurements, so compute is clearly relevant. However, the current project should not assume compute is the root bottleneck without ruling out power, thermal, memory, scheduler, or workload-shape effects.

### Evidence supporting relevance

- Existing GPU experiments measured utilization, power, temperature, and performance.
- Some workloads sustained high GPU utilization, which makes compute pressure plausible.

### Evidence against or limitations

- High utilization is a symptom, not proof of compute bottleneck.
- Current evidence is mostly single-GPU and does not fully separate compute limits from power, thermal, or memory effects.

### Unknowns

- Whether future target workloads are compute-heavy, memory-heavy, or communication-heavy.
- Whether utilization reflects useful work or stalled execution.
- Whether more detailed metrics would show memory or synchronization stalls.

### Expansion trigger

Expand compute-specific logic when repeated experiments show high utilization, stable thermals, stable power behavior, and poor throughput scaling after other resource explanations are checked.

---

## 2. Memory

### Definition

Memory means GPU VRAM, system RAM, memory bandwidth, memory capacity, allocation pressure, and data movement between memory levels.

### Bottleneck symptoms

- GPU utilization drops even though the workload should be active.
- Throughput changes sharply with batch size or model size.
- Runs fail or slow down near memory capacity.
- Workloads show stalls that are not explained by storage or network.

### Measurements that support this bottleneck

- VRAM usage near capacity
- memory bandwidth saturation
- out-of-memory failures
- high host memory pressure
- repeated slowdowns when memory footprint increases

### Measurements that weaken this bottleneck

- low memory usage
- no correlation between memory footprint and throughput
- bottleneck symptoms disappear when scheduler, storage, power, or thermal issues are addressed

### Software controllability

Medium. Software can adjust placement, batch size, caching, data layout, memory-heavy workload pairing, and sometimes precision. It cannot change physical memory capacity without different hardware.

### Current confidence

Low.

Memory is a plausible future bottleneck, but the current project has not yet collected enough memory-specific evidence to treat it as an active diagnosis target.

### Evidence supporting relevance

- AI workloads often depend on memory capacity and memory movement.
- Placement decisions may need to avoid pairing workloads that compete for memory capacity or bandwidth.

### Evidence against or limitations

- Current project evidence does not yet include detailed memory bandwidth or memory pressure measurements.
- Existing single-GPU power/performance data does not prove memory bottlenecks.

### Unknowns

- Whether target workloads saturate VRAM bandwidth.
- Whether VRAM capacity limits job placement.
- Whether memory-heavy jobs interfere when colocated.

### Expansion trigger

Expand into memory bottleneck logic when diagnosis repeatedly returns `unknown` for high-utilization or unstable-throughput workloads and memory-capacity or bandwidth data appears necessary to explain the result.

---

## 3. Storage

### Definition

Storage means local disk, network-attached storage, object storage, filesystem behavior, read/write throughput, and read/write latency.

### Bottleneck symptoms

- GPU utilization has idle gaps while data is loaded.
- Training or benchmark throughput is inconsistent between runs.
- Startup, checkpointing, logging, or dataset loading dominates runtime.
- Increasing compute resources does not improve throughput because data is not available fast enough.

### Measurements that support this bottleneck

- low GPU utilization during data-loading phases
- high disk utilization or I/O wait
- slow dataset reads
- slow checkpoint writes
- throughput improves after caching or preloading

### Measurements that weaken this bottleneck

- dataset already cached in memory
- storage latency is low during slowdown periods
- GPU remains compute-saturated without data-loading gaps

### Software controllability

Medium. Software can cache, prefetch, batch reads, change data layout, stage data locally, reduce checkpoint frequency, and schedule jobs near data. It cannot fix all physical storage limits.

### Current confidence

Low.

Storage is important for many systems, but the current project has not yet collected storage metrics.

### Evidence supporting relevance

- Any placement product eventually needs to know whether jobs are waiting on data rather than compute.
- Storage bottlenecks can create symptoms that look like GPU underuse.

### Evidence against or limitations

- Current GPU experiments do not include storage-specific evidence.
- The current product wedge can start without storage control if initial workloads are not storage-bound.

### Unknowns

- Whether target workloads stream large datasets.
- Whether checkpointing creates stalls.
- Whether storage delays correlate with GPU idle time.

### Expansion trigger

Expand into storage when low GPU utilization or inconsistent runtime correlates with data-loading, checkpoint, filesystem, or object-store behavior.

---

## 4. Network

### Definition

Network means communication between hosts, GPUs, storage systems, and services. This includes distributed training traffic, data transfer, remote storage access, and coordination traffic.

### Bottleneck symptoms

- Distributed jobs spend time waiting for communication.
- GPUs go idle during synchronization or data exchange.
- Jobs perform differently depending on node placement.
- Adding more GPUs produces weak scaling because communication cost grows.

### Measurements that support this bottleneck

- high network throughput near link limits
- high network latency
- communication phases align with GPU idle periods
- performance changes based on node topology or placement
- distributed workload traces show all-reduce or synchronization stalls

### Measurements that weaken this bottleneck

- single-node workloads with no meaningful network traffic
- GPU remains compute-saturated
- communication time is small relative to compute time

### Software controllability

Medium-to-high for placement and routing decisions. Low for physical bandwidth unless the system can choose different hardware or topology.

### Current confidence

Low.

Network is probably important later for distributed systems, but it is not yet proven by the current single-GPU evidence.

### Evidence supporting relevance

- The long-term product direction includes placement and resource coordination.
- Distributed AI workloads can be sensitive to communication and topology.

### Evidence against or limitations

- Current project evidence is not distributed-cluster evidence.
- Network bottlenecks should not be assumed from single-GPU benchmark results.

### Unknowns

- Whether target workloads are distributed.
- Whether communication time dominates or only occasionally spikes.
- Whether placement decisions can reduce network cost.

### Expansion trigger

Expand into network when distributed workload evidence shows communication stalls, topology-sensitive performance, or GPU idle time aligned with communication phases.

---

## 5. Power

### Definition

Power means electrical draw, power caps, power budgets, power throttling, and the relationship between energy use and useful throughput.

### Bottleneck symptoms

- GPU clocks or performance change near power limits.
- Lower power caps reduce power draw with small or workload-dependent performance changes.
- Performance-per-watt changes significantly across power settings.
- Multiple jobs together risk exceeding power budgets.

### Measurements that support this bottleneck

- power draw near configured limit
- power-limit throttle indicators if available
- clock reduction correlated with power cap
- throughput or efficiency changes across power settings
- repeated behavior across workloads

### Measurements that weaken this bottleneck

- power draw far below limit during slowdown
- no performance or clock relationship to power settings
- thermal, memory, storage, or scheduler evidence explains the slowdown better

### Software controllability

Medium. Software can set power caps, schedule workloads to smooth power, avoid high-power colocations, and report efficiency tradeoffs. It cannot change facility power capacity.

### Current confidence

Low-to-medium.

The project has prior power-cap experiments, so power is more grounded than many other future domains. Still, power should be treated as a relevant factor, not automatically the root bottleneck.

### Evidence supporting relevance

- Prior project experiments varied GPU power behavior and measured performance/efficiency outcomes.
- Power settings appeared relevant to throughput-per-watt behavior.

### Evidence against or limitations

- Prior power experiments do not prove power is always the limiting resource.
- Some workloads may be compute, memory, or thermal limited instead.
- Single-GPU power evidence does not automatically prove cluster-level power smoothing value.

### Unknowns

- Whether target production workloads hit power limits.
- Whether power caps improve cost/performance under realistic workloads.
- Whether power smoothing matters before multi-node or multi-GPU evidence exists.

### Expansion trigger

Expand power logic when repeated experiments show throughput, clocks, or efficiency changing predictably with power limits or when placement decisions need to avoid power-budget conflicts.

---

## 6. Cooling

### Definition

Cooling means the environment's ability to remove heat: airflow, fans, rack layout, room temperature, intake temperature, exhaust behavior, and facility cooling capacity.

### Bottleneck symptoms

- Many devices heat up together under sustained load.
- Performance degrades over longer runs.
- Fan behavior or ambient temperature changes correlate with performance.
- Thermal symptoms appear even when software workload is unchanged.

### Measurements that support this bottleneck

- rising ambient or intake temperature
- increasing fan speeds across devices
- correlated temperature rise across a rack or room
- thermal throttling after sustained load
- performance improves when airflow/cooling changes

### Measurements that weaken this bottleneck

- device temperatures remain stable and below throttle thresholds
- performance degrades without temperature movement
- power, scheduler, memory, or workload effects explain the behavior better

### Software controllability

Low-to-medium. Software can spread heat-producing workloads, reduce power caps, schedule cooldown periods, or alert humans. It usually cannot directly fix airflow or facility cooling.

### Current confidence

Low.

Cooling is a plausible infrastructure bottleneck, but the current project has not yet collected environmental or rack-level evidence.

### Evidence supporting relevance

- Cooling can limit sustained compute performance in real infrastructure.
- Placement and power decisions may need to avoid concentrating heat.

### Evidence against or limitations

- Current experiments do not prove a cooling bottleneck.
- Single-device temperature data is not enough to diagnose facility cooling limits.

### Unknowns

- Ambient temperature.
- Fan behavior.
- Airflow patterns.
- Whether long runs show heat accumulation.

### Expansion trigger

Expand into cooling only when sustained-load evidence shows temperature accumulation across devices or locations, especially when performance changes correlate with environmental conditions.

---

## 7. Thermal

### Definition

Thermal means device-level temperature behavior and temperature-induced performance reduction.

Cooling is the environment's ability to remove heat. Thermal is the device's actual temperature and throttle behavior.

### Bottleneck symptoms

- GPU temperature rises toward throttle range.
- Clock frequency drops as temperature rises.
- Performance is good early in a run and worse later.
- Re-running after cooldown improves performance.

### Measurements that support this bottleneck

- device temperature near throttle threshold
- thermal throttle indicators if available
- clock drops correlated with temperature rise
- performance degradation over time during sustained runs

### Measurements that weaken this bottleneck

- temperature remains stable and safe
- clocks do not drop as temperature changes
- performance changes occur without temperature movement

### Software controllability

Medium. Software can reduce power, change workload placement, avoid long sustained heat concentration, schedule cooldown windows, and warn operators.

### Current confidence

Low-to-medium.

Prior experiments include GPU temperature, so thermal is observable. However, current evidence should not claim thermal bottleneck unless temperature and clock/performance movement align.

### Evidence supporting relevance

- Prior project experiments measured temperature alongside power and performance.
- Thermal behavior is directly connected to sustained GPU operation.

### Evidence against or limitations

- Temperature measurement alone is not enough; it must correlate with throttling or performance loss.
- The current project has not yet established repeated thermal-throttle cases.

### Unknowns

- Actual throttle thresholds for each device and environment.
- Whether temperature explains performance variance better than power or workload shape.
- Whether longer runs produce different thermal behavior than short tests.

### Expansion trigger

Expand thermal logic when repeated runs show temperature-correlated clock drops, performance degradation, or throttle flags.

---

## 8. Scheduler

### Definition

Scheduler means the system that decides which job runs where, when, and with what colocated workloads or resource limits.

### Bottleneck symptoms

- Hardware exists but jobs wait or run in bad places.
- Certain workload pairings interfere with each other.
- Throughput changes depending on placement.
- Jobs receive resources that do not match their workload shape.

### Measurements that support this bottleneck

- placement history
- queue time
- job start/end time
- resource assignment
- colocated workload list
- performance changes across placements
- repeated bad pairings

### Measurements that weaken this bottleneck

- workload performance is stable across placements
- no co-location or queueing issue exists
- resource pressure is caused by hardware limits independent of placement

### Software controllability

High. This is one of the most controllable domains because software can recommend, block, explain, or change placement decisions.

### Current confidence

Low.

Scheduler relevance is central to the product wedge, but the current project has not yet collected enough placement history or multi-job evidence to prove scheduler-caused bottlenecks.

### Evidence supporting relevance

- The product wedge is load placement and avoidance.
- Diagnosis and reporting artifacts are being built to support future placement explanations.

### Evidence against or limitations

- Current experiments mostly show workload behavior, not scheduler behavior.
- Without placement records, scheduler bottleneck claims would be speculative.

### Unknowns

- Which workload pairings are harmful.
- Whether bad placement happens often enough to matter.
- What scheduler inputs are available in a real environment.

### Expansion trigger

Expand scheduler logic when experiments or real workload records show placement-sensitive performance, interference, bad pairings, or queue/resource mismatch.

---

## 9. Human workflow

### Definition

Human workflow means the operational process around experiments, diagnosis, reporting, review, and decision-making.

### Bottleneck symptoms

- Engineers cannot quickly explain why performance changed.
- Experiments are hard to reproduce.
- Reports are inconsistent or manual.
- Decisions depend on memory instead of artifacts.
- Debugging takes longer than the actual system change.

### Measurements that support this bottleneck

- repeated manual steps
- unclear experiment records
- missing reports
- inconsistent commands
- long time from observation to diagnosis
- repeated confusion about artifact ownership

### Measurements that weaken this bottleneck

- workflows are reproducible
- reports are generated consistently
- diagnosis outputs are clear
- future modules can reuse artifacts without re-learning the context

### Software controllability

High. Documentation, scripts, templates, validation, reports, and workflow automation can reduce this bottleneck directly.

### Current confidence

Medium.

This curriculum has repeatedly created reusable artifacts, checks, and handoff documents because human workflow itself can slow engineering progress.

### Evidence supporting relevance

- The project has already benefited from repeatable scripts, tests, docs, PR templates, and current-progress handoffs.
- The user explicitly wants structured workflows that reduce repeated prompt copying and lost context.

### Evidence against or limitations

- Human workflow improvements do not replace system telemetry or real bottleneck evidence.
- Better docs do not prove a GPU, scheduler, or power bottleneck.

### Unknowns

- Which manual steps consume the most time in future real environments.
- Whether workflow automation materially improves experiment throughput.
- Which handoffs need to become scripts versus remain docs.

### Expansion trigger

Expand human-workflow tooling when repeated module or experiment work shows that manual process, context loss, or inconsistent reporting is slowing progress more than technical implementation.

---

## 10. Heterogeneous device

### Definition

Heterogeneous device means systems with different kinds of compute devices: different GPU models, CPUs, accelerators, memory capacities, interconnects, or specialized hardware.

### Bottleneck symptoms

- A workload performs well on one device type and poorly on another.
- Scheduler assigns jobs to devices that do not match workload needs.
- Mixed hardware creates inconsistent performance or utilization.
- Device-specific limits dominate throughput or cost.

### Measurements that support this bottleneck

- per-device performance records
- device model and capability metadata
- memory capacity and bandwidth per device
- workload performance differences across devices
- cost/performance differences across device classes

### Measurements that weaken this bottleneck

- the environment has only one device type
- workload performance is stable across devices
- bottlenecks are explained by software or configuration rather than device mismatch

### Software controllability

High for routing and placement. Low for changing the physical capability of a device.

### Current confidence

Low.

This is a likely long-term concern, but current evidence is mostly single-device and does not justify heterogeneous-device logic yet.

### Evidence supporting relevance

- Future placement intelligence may need to match workload shape to device capability.
- Different devices can have different compute, memory, power, and thermal behavior.

### Evidence against or limitations

- Current project evidence does not include multiple GPU types or accelerator classes.
- Heterogeneous scheduling would be premature before single-device and single-resource evidence is stable.

### Unknowns

- Which device classes the product will target.
- Whether users have mixed hardware.
- Whether workload-device mismatch is common enough to justify implementation.

### Expansion trigger

Expand heterogeneous-device logic when real or simulated evidence shows performance, cost, or reliability changes based on device class or device-workload mismatch.

---

# Docs-only review checklist

Before this document is considered complete, verify:

- [ ] Every expected resource domain is included.
- [ ] Every domain defines what the resource means.
- [ ] Every domain lists bottleneck symptoms.
- [ ] Every domain lists measurements that support the bottleneck.
- [ ] Every domain lists measurements that weaken the bottleneck.
- [ ] Every domain states software controllability.
- [ ] Every domain states current confidence.
- [ ] Every domain includes evidence supporting relevance.
- [ ] Every domain includes evidence against or limitations.
- [ ] Every domain includes unknowns.
- [ ] Every domain includes an expansion trigger.
- [ ] No domain is claimed as proven without evidence.
- [ ] Module 12 diagnosis policy is referenced.
- [ ] Future reuse trigger is stated.

## Future reuse trigger

Audit this file whenever a future module adds or changes logic related to:

- bottleneck diagnosis
- placement recommendations
- scheduler decisions
- controller actions
- telemetry collection
- performance explanation
- thermal or power claims
- memory, storage, network, or heterogeneous-device expansion
