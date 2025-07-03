import os
import time
from datetime import datetime, timedelta, timezone

from service.utils.logger import logger


def generate_timestamp() -> tuple[str, str, str]:
    
    utc_now = datetime.now(timezone.utc)

    actual_hour = int(utc_now.timestamp())

    generation_time = utc_now.strftime("%Y-%m-%dT%H:%M:%SZ")
    expiration_time = (utc_now + timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ")

    path = "service/time/actual_hour_epoch.txt"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w', encoding='utf-8') as file:
        file.write(str(actual_hour))

    return actual_hour, generation_time, expiration_time