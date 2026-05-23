from gpu_lab.summary import calculate_summary

samples = [
    {"timestamp": "12:00", "power": 100, "temp": 70, "utilization": 80},
    {"timestamp": "12:01", "power": 120, "temp": 65, "utilization": 90},
    {"timestamp": "12:02", "power": 140, "temp": 60, "utilization": 95},
]
summary = calculate_summary(samples)

assert summary["sample_count"] == 3
assert summary["avg_power"] == 120
assert summary["avg_temp"] == 65
assert summary["avg_utilization"] == 88.33333333333333
assert summary["min_power"] == 100
assert summary["max_power"] == 140
assert summary["min_temp"] == 60
assert summary["max_temp"] == 70