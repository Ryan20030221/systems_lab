from gpu_lab.models import GpuSample


def test_gpu_samples_stores_fields():
    sample = GpuSample("12:00", 140, 68, 95)
    assert sample.timestamp == "12:00"
    assert sample.power == 140
    assert sample.temp == 68
    assert sample.utilization == 95


def test_gpu_sample_is_active_above_threshold():
    sample = GpuSample("12:00", 140, 68, 95)
    assert sample.is_active(92)


def test_gpu_sample_is_active_at_threshold():
    sample = GpuSample("12:00", 140, 68, 95)
    assert sample.is_active(95)


def test_gpu_sample_is_not_active_below_threshold():
    sample = GpuSample("12:00", 140, 68, 95)
    assert not sample.is_active(98)
