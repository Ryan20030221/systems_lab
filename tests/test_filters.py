from gpu_lab.filters import filter_active_samples


def test_filter_active_samples():
    samples = [
        {
            "power": 40,
            "temp": 45,
            "utilization": 2,
            "workload": "idle",
            "power_mode": "100%",
        },
        {
            "power": 145,
            "temp": 70,
            "utilization": 95,
            "workload": "furmark",
            "power_mode": "100%",
        },
        {
            "power": 150,
            "temp": 72,
            "utilization": 98,
            "workload": "furmark",
            "power_mode": "80%",
        },
    ]

    active = filter_active_samples(samples, 50)

    assert len(active) == 2
    assert active[0]["power"] == 145
    assert active[1]["utilization"] == 98
