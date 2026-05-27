import time
from datetime import datetime, timezone


def utc_timestamp_for_filename():
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")


def start_timer():
    return time.perf_counter()


def elapsed_seconds(start):
    return time.perf_counter() - start
