import os
from service.utils.logger import logger


def timestamp_exists() -> bool:

    time_path = "service/time/actual_hour_epoch.txt"
    
    if os.path.exists(time_path):
        logger.debug("Timestamp exists")
        return True
    else:
        logger.debug("Timestamp not exists")
        return  False
