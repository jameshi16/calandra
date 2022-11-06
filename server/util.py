# util.py - Utility functions
from datetime import datetime

# date: Will only extract year, month, day
# time_str: will extract hour & minute
def pt_timedate_to_str(date, time_str):
    time_tuple = time_str.split(':')
    return datetime(date.year, date.month, date.day,
                    hour=int(time_tuple[0]),
                    minute=int(time_tuple[1])).isoformat()
