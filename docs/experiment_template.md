# Experiment Template

## 1. Experiment Metadata
- Experiment ID:
- Date:
- Author:
- Machine / GPU:
- Workload:

## 2. Experiment Question
What exact question is this experiment trying to answer?

## 3. Hypothesis
What do you expect to happen before running the experiment?

## 4. Baseline
What result or setting is used as the comparison point?

## 5. Independent Variable
What is the one main variable intentionally changed?

## 6. Dependent Variables
What measured outputs will be compared?

Examples:
- avg_power_w
- avg_temp_c
- avg_utilization_pct
- avg_clock_mhz
- performance_score
- perf_loss_pct
- power_savings_pct

## 7. Control Variables
What conditions stay the same so the comparison is fair?

Examples:
- same workload
- same test duration
- same warmup period
- same logging interval
- same GPU
- same driver
- same performance metric

## 8. Warmup Plan
How much early data should be ignored before the run is considered stable?

## 9. Repeated Trials Plan
How many trials will be run for each condition?

## 10. Procedure
What exact steps will be followed to run the experiment?

## 11. Data Collection Plan
What logs, manual readings, or output files will be collected?

## 12. Success Criteria
What result would count as a successful experiment?

Example:
Accept the lower power mode if performance loss is <= 5% and power savings are >= 10%.

## 13. Results
What measured values were observed?

## 14. Conclusion
What conclusion is supported by the results?

## 15. Limitations
What weaknesses, assumptions, or uncontrolled factors could affect the result?

## 16. Reproducibility Checklist
- [ ] Workload recorded
- [ ] Power mode recorded
- [ ] Baseline recorded
- [ ] Duration recorded
- [ ] Warmup recorded
- [ ] Trial count recorded
- [ ] Metrics use clear units
- [ ] Procedure is repeatable
- [ ] Limitations are documented
