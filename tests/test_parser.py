from gpu_lab.parser import parse_gpu_rows, load_lines


def test_parse_gpu_rows_valid_rows():

    
    lines = [
        "timestamp,power,temp,utilization",
        "12:00,140,68,95",
        "12:01,145,70,97",
    ]


    samples = parse_gpu_rows(lines)

    assert len(samples) == 2
    assert samples[0]["timestamp"] == "12:00"
    assert samples[0]["power"] == 140
    assert samples[1]["utilization"] == 97

def test_load_lines(tmp_path):
    log_path = tmp_path / "fake_gpu_log.csv"
    log_path.write_text("timestamp,power,temp,utilization\n12:00,140,68,95\n",encoding="utf-8")
    lines = load_lines(log_path)
    assert(len(lines)==2)
    assert lines[0] == "timestamp,power,temp,utilization\n"
    assert lines[1] == "12:00,140,68,95\n"


