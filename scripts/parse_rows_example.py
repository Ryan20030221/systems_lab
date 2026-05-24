lines = [
    "timestamp,power,temp,utilization",
    "12:00,140,68,95",
    "12:01,145,70,97",
]


def parse_rows(lines):
    samples = []

    for line in lines[1:]:
        parts = line.strip().split(",")

        sample = {
            "timestamp": parts[0],
            "power": int(parts[1]),
            "temp": int(parts[2]),
            "utilization": int(parts[3]),
        }

        samples.append(sample)

    return samples


samples = parse_rows(lines)

print(samples)

assert len(samples) == 2
assert samples[0]["power"] == 140
assert samples[1]["utilization"] == 97
