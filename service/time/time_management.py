import os
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from service.utils.logger import logger


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


def is_token_expired() -> bool:
    current_timestamp = int(time.time())
    path = "service/time/actual_hour_epoch.txt"

    with open(path, 'r', encoding='utf-8') as file:
        token_timestamp = int(file.read())

    logger.debug("Current timestamp:", current_timestamp)
    logger.debug("Token timestamp:", token_timestamp)

    time_difference = token_timestamp - current_timestamp
    logger.debug("Time difference in seconds:", time_difference)

    MAX_ALLOWED_DIFFERENCE = 43200  # 12 hours in seconds

    # Return True if the token is expired (too old or too far in future)
    if abs(time_difference) > MAX_ALLOWED_DIFFERENCE:
        return True
    else:
        return False
