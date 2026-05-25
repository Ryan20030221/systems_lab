from dataclasses import dataclass


@dataclass
class GpuSample:
    timestamp: str
    power: int
    temp: int
    utilization: int

    def is_active(self, min_utilization: int) -> bool:
        return self.utilization >= min_utilization


sample = GpuSample(timestamp="12:00", power=140, temp=68, utilization=95)

print(sample)
print(sample.power)
print(sample.is_active(50))
print(sample.is_active(99))

sample = GpuSample("12:00", 140, 68, 95)

assert sample.timestamp == "12:00"
assert sample.power == 140
assert sample.temp == 68
assert sample.utilization == 95
assert sample.is_active(50) is True
assert sample.is_active(95) is True
assert sample.is_active(96) is False
