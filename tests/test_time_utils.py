import re
import time

from gpu_lab.time_utils import elapsed_seconds, start_timer, utc_timestamp_for_filename


def test_utc_timestamp_returns_filename_safe_string():
    timestamp = utc_timestamp_for_filename()

    assert isinstance(timestamp, str)
    assert re.match(r"^\d{8}_\d{6}_\d{6}$", timestamp)
    assert " " not in timestamp
    assert ":" not in timestamp


def test_start_timer_returns_float():
    start = start_timer()
    assert isinstance(start, float)
    assert start > 0


def test_start_timer_and_elapsed_seconds_return_nonnegative_duration():
    start = start_timer()
    time.sleep(0.003)
    duration = elapsed_seconds(start)
    assert duration >= 0
    assert isinstance(duration, float)
