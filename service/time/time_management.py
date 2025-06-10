import os
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def generate_timestamp() -> tuple[str, str, str]:

    baires_tz = ZoneInfo("America/Argentina/Buenos_Aires")
    actual_hour = int(time.time())
    generation_time = datetime.now(baires_tz).strftime("%Y-%m-%dT%H:%M:%S")
    expiration_time = (datetime.now(baires_tz) + timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%S")

    path = "service/time/actual_hour_epoch.txt"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w', encoding='utf-8') as file:
        file.write(str(actual_hour))

    return actual_hour, generation_time, expiration_time

def compare_time() -> bool:

    actual_hour = int(time.time())
    path = "service/time/actual_hour_epoch.txt"

    with open(path, 'r', encoding='utf-8') as file:
        token_request_hour = int(file.read())

    hours_difference = actual_hour - token_request_hour

    if hours_difference > 0:

        return False # Token is valid yet
    else:
        
        return True # Token isn't valid
