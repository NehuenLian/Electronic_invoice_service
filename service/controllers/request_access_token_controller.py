from service.crypto.sign import get_binary_cms, sign_login_ticket_request
from service.soap_handler.soap_client import login_cms
from service.utils.logger import logger
from service.xml_management.xml_builder import (
    build_login_ticket_request, parse_and_save_loginticketresponse, save_xml)


def generate_token_from_scratch():

    root = build_login_ticket_request()
    save_xml(root, "loginTicketRequest.xml")
    sign_login_ticket_request()
    b64_cms = get_binary_cms()
    login_ticket_response = login_cms(b64_cms)
    parse_and_save_loginticketresponse(login_ticket_response)
    logger.info("Token generated.")

def generate_token_from_existing():

    logger.info("Token still valid. Generating loginTicketResponse without signing or creating new loginTicketRequest.")
    b64_cms = get_binary_cms()
    login_ticket_response = login_cms(b64_cms)
    parse_and_save_loginticketresponse(login_ticket_response)
    logger.info("Token generated.")