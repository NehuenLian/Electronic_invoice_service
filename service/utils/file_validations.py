import os

from service.utils.logger import logger


def xml_exists(xml_name: str) -> bool:
    xml_path = f"service/xml_management/xml_files/{xml_name}"

    if os.path.exists(xml_path):
        return True
    else:
        return False
