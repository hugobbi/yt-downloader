import time
from typing import List

def get_current_time_string() -> str:
    current_time = time.localtime()
    return f'{current_time.tm_year}-{current_time.tm_mon}-{current_time.tm_mday}_{current_time.tm_hour}-{current_time.tm_min}-{current_time.tm_sec}'

def get_time_milliseconds(time: List[int]) -> int:
    return time[0] * 3600000 + time[1] * 60000 + time[2] * 1000
