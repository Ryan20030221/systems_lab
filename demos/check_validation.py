from gpu_lab.validation import is_valid_utilization, validate_sample

valid_sample = {
    "timestamp": "12:00",
    "power": 140,
    "temp": 68,
    "utilization": 95,
}

invalid_utilization_sample = {
    "timestamp": "12:01",
    "power": 140,
    "temp": 68,
    "utilization": 101,
}

missing_key_sample = {
    "timestamp": "12:02",
    "power": 140,
    "temp": 68,
}

assert validate_sample(valid_sample) is True
assert validate_sample(invalid_utilization_sample) is False
assert validate_sample(missing_key_sample) is False

assert is_valid_utilization(-1) is False
assert is_valid_utilization(0) is True
assert is_valid_utilization(50) is True
assert is_valid_utilization(100) is True
assert is_valid_utilization(101) is False

print("validation checks passed")
