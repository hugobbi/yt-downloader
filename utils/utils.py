import time

def get_current_time_string() -> str:
    current_time = time.localtime()
    return f'{current_time.tm_year}-{current_time.tm_mon}-{current_time.tm_mday}_{current_time.tm_hour}-{current_time.tm_min}-{current_time.tm_sec}'
