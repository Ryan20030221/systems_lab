A dataclass is useful when project data has a known shape.
A dictionary is better when data is flexible, temporary, or unknown.
Models should describe data, but validation.py should still decide whether values are valid.
Not everything should become a class because too many classes can make simple code harder to read.
