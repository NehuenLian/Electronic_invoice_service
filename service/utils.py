import os


def timestamp_exists():
    time_path = "service/time/actual_hour_epoch.txt"
    
    if os.path.exists(time_path):
        return True
    else:
        return  False
