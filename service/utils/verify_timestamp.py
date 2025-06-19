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

def login_ticket_response_exists() -> bool:
    xml_path = "service/xml_management/loginTicketResponse.xml"

    if os.path.exists(xml_path):
        logger.debug("loginTicketResponse exists")
        return True
    else:
        logger.debug("loginTicketResponse not exists")
        return False