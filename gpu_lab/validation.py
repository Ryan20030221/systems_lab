

def is_valid_utilization(value):
    return (type(value) is int) and 0<= value <=100

def is_valid_power(value):
    return (type(value) is int or type(value) is float) and 0<=value

def is_valid_temperature(value):
    return (type(value) is int or type(value) is float) and 0<= value <= 120

def validate_sample(sample):
    required_keys = ["timestamp", "power", "temp", "utilization"]

    for key in required_keys:
        if key not in sample:
            return False
    
    return (is_valid_power(sample["power"])
    and is_valid_utilization(sample["utilization"])
    and is_valid_temperature(sample["temp"]))

