from gpu_lab.parser import parse_gpu_rows

lines = [
    "timestamp,power,temp,utilization",
    "12:00,140,68,95",
    "12:01,145,70,97",
    "12:02,150,72,98",
]

samples = parse_gpu_rows(lines)

print(samples)


assert len(samples) == 3
assert samples[0]["timestamp"] == "12:00"
assert samples[0]["power"] == 140
assert samples[2]["temp"] == 72
assert samples[2]["utilization"] == 98
assert samples[0]["timestamp"] != "timestamp"
