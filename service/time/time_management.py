from datetime import datetime, timedelta, timezone

import ntplib
from service.utils.logger import logger


def generate_ntp_timestamp() -> tuple[int, str, str]:

    logger.debug("Consulting NTP for get the datetime...")

    client = ntplib.NTPClient()
    response = client.request('time.afip.gov.ar')

    generation_dt = datetime.fromtimestamp(response.tx_time, tz=timezone.utc)

    actual_time_epoch = int(generation_dt.timestamp())

    expiration_dte = generation_dt + timedelta(minutes=10)

    generation_time = generation_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    expiration_time = expiration_dte.strftime('%Y-%m-%dT%H:%M:%SZ')

    logger.debug(f"Datetime values: epoch: {actual_time_epoch} | gentime: {generation_time} | exptime: {expiration_time}")

    return actual_time_epoch, generation_time, expiration_time
