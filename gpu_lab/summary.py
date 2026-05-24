def calculate_summary(samples):

    count = len(samples)

    if count == 0:
        return {
            "sample_count": 0,
            "avg_power": None,
            "avg_temp": None,
            "avg_utilization": None,
            "min_power": None,
            "max_power": None,
            "min_temp": None,
            "max_temp": None,
        }
    total_power = 0
    total_temp = 0
    total_utilization = 0
    min_power = samples[0]["power"]
    max_power = samples[0]["power"]
    min_temp = samples[0]["temp"]
    max_temp = samples[0]["temp"]
    for sample in samples:
        total_power += sample["power"]
        total_temp += sample["temp"]
        total_utilization += sample["utilization"]
        if sample["power"] > max_power:
            max_power = sample["power"]
        if sample["power"] < min_power:
            min_power = sample["power"]
        if sample["temp"] > max_temp:
            max_temp = sample["temp"]
        if sample["temp"] < min_temp:
            min_temp = sample["temp"]

    summary = {
        "sample_count": count,
        "avg_power": total_power / count,
        "avg_temp": total_temp / count,
        "avg_utilization": total_utilization / count,
        "min_power": min_power,
        "max_power": max_power,
        "min_temp": min_temp,
        "max_temp": max_temp,
    }

    return summary
