from dataclasses import dataclass


@dataclass(frozen=True)
class GpuSample:
    timestamp: str
    power: int | float
    temp: int | float
    utilization: int

    def is_active(self, min_utilization: int) -> bool:
        return self.utilization >= min_utilization
