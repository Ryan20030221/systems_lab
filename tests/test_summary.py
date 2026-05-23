from gpu_lab.summary import calculate_summary

def test_summary():
    samples = [
        {"power": 100, "temp": 60, "utilization": 50},
        {"power": 200, "temp": 80, "utilization": 100},
    ]

    summary = calculate_summary(samples)

    assert summary["sample_count"] == 2
    assert summary["avg_power"] == 150
    assert summary["avg_temp"] == 70
    assert summary["avg_utilization"] == 75
    assert summary["min_power"] == 100
    assert summary["max_power"] == 200
    assert summary["min_temp"] == 60
    assert summary["max_temp"] == 80

    empty_summary = calculate_summary([])

    assert empty_summary["sample_count"] == 0
    assert empty_summary["avg_power"] is None

