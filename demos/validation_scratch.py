samples = [
    {"timestamp": "12:00", "utilization": 95},
    {"timestamp": "12:01", "utilization": -1},
    {"timestamp": "12:02", "utilization": 101},
    {"timestamp": "12:03", "utilization": "bad"},
]


def is_valid_utilization(value):

    if not isinstance(value, int):
        return False

    if value > 100:
        return False

    if value < 0:
        return False

    return True


def validate_simple_sample(samples):
    valid_samples = []
    invalid_samples = []
    for sample in samples:
        if is_valid_utilization(sample["utilization"]):
            valid_samples.append(sample)
        else:
            invalid_samples.append(sample)

    return valid_samples, invalid_samples


valid, invalid = validate_simple_sample(samples)

print("valid samples", valid)
print("invalid smaples", invalid)

assert is_valid_utilization(-1) is False
assert is_valid_utilization(0) is True
assert is_valid_utilization(50) is True
assert is_valid_utilization(100) is True
assert is_valid_utilization(101) is False
assert is_valid_utilization("bad") is False

valid, invalid = validate_simple_sample(samples)

assert len(valid) == 1
assert len(invalid) == 3
assert valid[0]["utilization"] == 95
assert invalid[0]["utilization"] == -1
assert invalid[1]["utilization"] == 101
assert invalid[2]["utilization"] == "bad"

print("All checks passed")
