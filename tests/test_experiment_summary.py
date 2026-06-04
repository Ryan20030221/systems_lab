import pytest

from gpu_lab.experiment_summary import load_experiment_summaries

VALID_CSV = (
    "experiment_name,sample_count,avg_power,avg_temp,avg_utilization,"
    "min_power,max_power,min_temp,max_temp\n"
    "baseline,100,150.0,72.5,85.0,120.0,180.0,65.0,80.0\n"
)


def test_happy_path(tmp_path):
    csv_file = tmp_path / "summary.csv"
    csv_file.write_text(VALID_CSV, encoding="utf-8")

    result = load_experiment_summaries(csv_file)

    assert len(result) == 1
    row = result[0]
    assert row["experiment_name"] == "baseline"
    assert isinstance(row["experiment_name"], str)
    assert row["sample_count"] == 100
    assert isinstance(row["sample_count"], int)
    assert row["avg_power"] == 150.0
    assert isinstance(row["avg_power"], float)


def test_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_experiment_summaries(tmp_path / "nonexistent.csv")


def test_path_is_directory(tmp_path):
    with pytest.raises(ValueError, match="not a file"):
        load_experiment_summaries(tmp_path)


def test_empty_file_no_header(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="no header row"):
        load_experiment_summaries(csv_file)


def test_header_only_no_data_rows(tmp_path):
    csv_file = tmp_path / "header_only.csv"
    csv_file.write_text(
        "experiment_name,sample_count,avg_power,avg_temp,avg_utilization,"
        "min_power,max_power,min_temp,max_temp\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="no data rows"):
        load_experiment_summaries(csv_file)


def test_missing_required_column(tmp_path):
    csv_file = tmp_path / "missing_col.csv"
    csv_file.write_text(
        "experiment_name,sample_count,avg_power\nbaseline,100,150.0\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        load_experiment_summaries(csv_file)


def test_bad_cell_type(tmp_path):
    csv_file = tmp_path / "bad_type.csv"
    csv_file.write_text(
        "experiment_name,sample_count,avg_power,avg_temp,avg_utilization,"
        "min_power,max_power,min_temp,max_temp\n"
        "baseline,100,NOT_A_FLOAT,72.5,85.0,120.0,180.0,65.0,80.0\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="avg_power"):
        load_experiment_summaries(csv_file)
