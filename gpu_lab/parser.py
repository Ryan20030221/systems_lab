def load_lines(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.readlines()


def parse_gpu_rows(lines):
    samples = []

    for line in lines[1:]:
        line = line.strip()

        if line == "":
            continue
        parts = line.split(",")

        sample = {
            "timestamp": parts[0],
            "power": int(parts[1]),
            "temp": int(parts[2]),
            "utilization": int(parts[3]),
        }

        samples.append(sample)
    return samples
