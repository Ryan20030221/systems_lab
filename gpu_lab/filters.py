


def filter_active_samples(samples, min_utilization):
    active_samples = []
    for sample in samples:
        if sample["utilization"]>= min_utilization:
            active_samples.append(sample)
    
    return active_samples


def filter_by_workload(samples, workload):
    workload_samples = []
    for sample in samples:
        if sample["workload"] == workload:
            workload_samples.append(sample)
    
    return workload_samples

def filter_by_power_mode(samples, power_mode):
    power_mode_samples = []
    for sample in samples:
        if sample["power_mode"] == power_mode:
            power_mode_samples.append(sample)
    
    return power_mode_samples

def get_unique_values(samples, key):
    unique_values = set()
    for sample in samples:
        unique_values.add(sample[key])
    
    return unique_values

