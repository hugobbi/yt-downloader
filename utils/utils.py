import time
import os
from typing import List

def get_current_time_string() -> str:
    current_time = time.localtime()
    return f'{current_time.tm_year}-{current_time.tm_mon}-{current_time.tm_mday}_{current_time.tm_hour}-{current_time.tm_min}-{current_time.tm_sec}'

def get_time_milliseconds(time: List[int]) -> int:
    return time[0] * 3600000 + time[1] * 60000 + time[2] * 1000

def get_latest_file(directory: str) -> str:
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    if not files:
        raise Exception(f"Error! No files found in the directory {directory}")
    
    latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(directory, f)))

    return latest_file
