samples = [
    {"power": 40, "utilization": 2, "tag": "idle"},
    {"power": 145, "utilization": 95, "tag": "active"},
    {"power": 150, "utilization": 98, "tag": "active"},
]


def filter_active_samples(samples, min_utilization):
    active_samples = []
    for sample in samples:
        if sample["utilization"] >= min_utilization:
            active_samples.append(sample)

    return active_samples


active_samples = filter_active_samples(samples, 50)

print(active_samples)
print("active count", len(active_samples))
