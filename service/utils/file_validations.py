import os

from service.utils.logger import logger


def timestamp_exists() -> bool:
    time_path = "service/time/actual_hour_epoch.txt"
    
    if os.path.exists(time_path):
        return True
    else:
        return  False
    
def login_ticket_request_exists() -> bool:
    xml_path = "service/xml_management/xml_files/loginTicketRequest.xml"

    if os.path.exists(xml_path):
        return True
    else:
        return False
    
def login_ticket_response_exists() -> bool:
    xml_path = "service/xml_management/xml_files/loginTicketResponse.xml"

    if os.path.exists(xml_path):
        return True
    else:
        return False