import os

from lxml import etree

from service.time.time_management import generate_timestamp

from service.utils.logger import logger



def build_login_ticket_request():

    root = etree.Element("loginTicketRequest")
    header = etree.SubElement(root, "header")
    unique_id = etree.SubElement(header, "uniqueId")
    generation_time_label = etree.SubElement(header, "generationTime")
    expiration_time_label = etree.SubElement(header, "expirationTime")
    service = etree.SubElement(root, "service")

    actual_hour, generation_time, expiration_time = generate_timestamp()

    unique_id.text = str(actual_hour)
    generation_time_label.text = str(generation_time)
    expiration_time_label.text = str(expiration_time)
    service.text = "wsfe"

    logger.debug("loginTicketRequest.xml was successfully built.")

    return root

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

    logger.debug("loginTicketResponse.xml was successfully built.")

    save_xml(root, "loginTicketResponse.xml")

    logger.debug("loginTicketResponse.xml saved in 'xml_management/' folder.")

def extract_token_and_sign_from_loginticketresponse(xml_name: str) -> tuple[str, str]:

    logger.debug("Extracting token and sign from loginTicketResponse.xml...")

    path = f"service/xml_management/{xml_name}"
    tree = etree.parse(path)
    root = tree.getroot()

    token_label = root.find(".//token")
    sign_label = root.find(".//sign")

    token = token_label.text
    sign = sign_label.text

    logger.debug("Token and Sign obtained successfully.")

    return token, sign

def save_xml(root, xml_name):
    
    path = f"service/xml_management/{xml_name}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tree = etree.ElementTree(root)
    tree.write(path, pretty_print=True, xml_declaration=True, encoding="UTF-8")
