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
