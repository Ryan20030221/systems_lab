# GPU Bottleneck Diagnosis Stack

## Purpose

This stack defines how the project converts validated experiment evidence into conservative GPU bottleneck diagnosis labels.

The goal is not to prove root causes from weak data. The goal is to produce the safest diagnosis that the available evidence supports.

A diagnosis result should answer:

- what symptom was observed
- what evidence supports it
- how confident the project is
- what competing explanations remain possible
- what limitations prevent stronger claims

This stack prepares future placement intelligence modules to explain why a workload placement may be good, risky, or inconclusive.

---

## Inputs

The diagnosis stack consumes structured experiment summary records.

The expected input shape comes from:

```python
from gpu_lab.experiment_summary import load_experiment_summaries
