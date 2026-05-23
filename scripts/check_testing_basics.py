
numbers = [10, 20, 30]

samples = [
    {"power": 40, "temp": 45, "utilization": 2},
    {"power": 145, "temp": 70, "utilization": 95},
    {"power": 150, "temp": 72, "utilization": 98},
]


def min_value(numbers):
    min_number = numbers[0]
    for number in numbers:
        if number < min_number:
            min_number = number
    return min_number

def max_value(numbers):
    max_number = numbers[0]
    for number in numbers:
        if number > max_number:
            max_number = number
    return max_number

def average(numbers):
    return sum(numbers) / len(numbers)

def filter_active_samples(samples, min_utilization):
    active_samples = []
    for sample in samples:
        if sample["utilization"] >= min_utilization:
            active_samples.append(sample)
    
    return active_samples
            
active_samples = filter_active_samples(samples, 50)
assert average(numbers) == 20
assert min_value(numbers) == 10
assert max_value(numbers) == 30
assert len(active_samples) == 2
assert active_samples[0]["power"] == 145
assert active_samples[1]["utilization"] == 98

print("basic testing checks passed")

