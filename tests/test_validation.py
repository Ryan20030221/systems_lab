from gpu_lab.validation import (
    is_valid_power,
    is_valid_temperature,
    is_valid_utilization,
    validate_sample,
)

def test_validation_utilization():


    assert is_valid_utilization(0) is True
    assert is_valid_utilization(50) is True
    assert is_valid_utilization(100) is True
    assert is_valid_utilization(-1) is False
    assert is_valid_utilization(101) is False
    assert is_valid_utilization("95") is False
def test_validation_power():
    assert is_valid_power(0) is True
    assert is_valid_power(140) is True
    assert is_valid_power(-1) is False
def test_validation_temperature():
    assert is_valid_temperature(0) is True
    assert is_valid_temperature(70) is True
    assert is_valid_temperature(120) is True
    assert is_valid_temperature(-1) is False
    assert is_valid_temperature(121) is False
def test_validation_sample():
    valid_sample = {
        "timestamp": "12:00",
        "power": 140,
        "temp": 68,
        "utilization": 95,
    }

    missing_key_sample = {
        "timestamp": "12:00",
        "power": 140,
        "temp": 68,
    }

    assert validate_sample(valid_sample) is True
    assert validate_sample(missing_key_sample) is False

  