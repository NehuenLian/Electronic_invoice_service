import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from lxml import etree

from service.time.time_management import generate_timestamp, generate_ntp_timestamp
from service.utils.logger import logger


def build_login_ticket_request():

    root = etree.Element("loginTicketRequest")
    header = etree.SubElement(root, "header")
    unique_id = etree.SubElement(header, "uniqueId")
    generation_time_label = etree.SubElement(header, "generationTime")
    expiration_time_label = etree.SubElement(header, "expirationTime")
    service = etree.SubElement(root, "service")

    actual_hour, generation_time, expiration_time = generate_ntp_timestamp()

    unique_id.text = str(actual_hour)
    generation_time_label.text = str(generation_time)
    expiration_time_label.text = str(expiration_time)
    service.text = "wsfe"

    return root

def build_comp_ultimo_autorizado():

    """
    This builder function corresponds to fe_comp_ultimo_autorizado (FECompUltimoAutorizado) Service.
    Te function build the necessary .xml file for this service.
    """

    pass

def parse_and_save_loginticketresponse(login_ticket_response: str):

    root = etree.fromstring(login_ticket_response.encode("utf-8"))
    header = etree.SubElement(root, "header")
    source = etree.SubElement(header, "source")
    destination = etree.SubElement(header, "destination")
    unique_id = etree.SubElement(header, "uniqueId")
    generation_time_label = etree.SubElement(header, "generationTime")
    expiration_time_label = etree.SubElement(header, "expirationTime")

    credentials = etree.SubElement(root, "credentials")
    token = etree.SubElement(credentials, "token")
    sign = etree.SubElement(credentials, "sign")

    save_xml(root, "loginTicketResponse.xml")

def extract_token_and_sign_from_loginticketresponse(xml_name: str) -> tuple[str, str]:

    path = f"service/xml_management/xml_files/{xml_name}"
    tree = etree.parse(path)
    root = tree.getroot()

    token_label = root.find(".//token")
    sign_label = root.find(".//sign")

    token = token_label.text
    sign = sign_label.text

    return token, sign

def is_expired(xml_name: str) -> bool:

    logger.debug(f"Running is_expired() function for {xml_name}")

    _, actual_hour, _ = generate_ntp_timestamp()

    actual_dt = datetime.strptime(str(actual_hour), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

    path = f"service/xml_management/xml_files/{xml_name}"
    tree = etree.parse(path)
    root = tree.getroot()
    expiration_time_label = root.find(".//expirationTime")
    expiration_time_str = expiration_time_label.text

    expiration_dt = datetime.strptime(expiration_time_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

    if actual_dt >= expiration_dt:
        return True
    else:
        return False

def save_xml(root, xml_name):
    
    path = f"service/xml_management/xml_files/{xml_name}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tree = etree.ElementTree(root)
    tree.write(path, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    logger.info(f"{xml_name} successfully saved.")