samples = [
    {"timestamp": "12:00", "power": 100, "temp": 60, "utilization": 80},
    {"timestamp": "12:01", "power": 120, "temp": 65, "utilization": 90},
    {"timestamp": "12:02", "power": 140, "temp": 70, "utilization": 95},
]


def calculate_basic_summary(samples):
    total_power = 0
    total_temp = 0
    max_temp = samples[0]["temp"]
    count = len(samples)
    for sample in samples:
        total_power += sample["power"]
        total_temp += sample["temp"]

        if sample["temp"] > max_temp:
            max_temp = sample["temp"]

    basic_summary = {
        "sample_count": count,
        "avg_power": total_power / count,
        "avg_temp": total_temp / count,
        "max_temp": max_temp,
    }
    return basic_summary


summary = calculate_basic_summary(samples)

assert summary["sample_count"] == 3
assert summary["avg_power"] == 120
assert summary["avg_temp"] == 65
assert summary["max_temp"] == 70

print("basic summary checks passed")
