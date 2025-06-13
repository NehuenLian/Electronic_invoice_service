from service.crypto.sign import get_binary_cms, sign_login_ticket_request
from service.json_management.convert_to_json import convert_zeep_object_to_dict
from service.payload_builder.builder import add_auth_to_payload
from service.soap_handler.soap_client import fecae_solicitar, login_cms
from service.time.time_management import is_token_expired
from service.utils.convert_model_to_dict import convert_pydantic_model_to_dict
from service.utils.logger import logger
from service.utils.verify_timestamp import timestamp_exists
from service.xml_management.xml_builder import (
    build_login_ticket_request,
    extract_token_and_sign_from_loginticketresponse,
    parse_and_save_loginticketresponse, save_xml)


def request_access_token():
    
    logger.info("Generating new token...")
    root = build_login_ticket_request()
    save_xml(root, "loginTicketRequest.xml")
    sign_login_ticket_request()
    b64_cms = get_binary_cms()
    login_ticket_response = login_cms(b64_cms)
    parse_and_save_loginticketresponse(login_ticket_response)
    logger.info("Process of requesting a token finished sucessfully.")

def generate_invoice(parsed_data: dict) -> dict:

    logger.info("Generating invoice...")
    token, sign = extract_token_and_sign_from_loginticketresponse("loginTicketResponse.xml")
    full_built_invoice  = add_auth_to_payload(parsed_data, token, sign)
    returned_cae = fecae_solicitar(full_built_invoice)
    logger.info("Invoice generated.")

    return returned_cae

def request_invoice_controller(parsed_data: dict) -> dict:

    logger.info("Checking if the timestamp value exists...")
    if not timestamp_exists():
        logger.info("Timestamp doesnt exist. Generating timestamp and requesting new token...")
        request_access_token()
        returned_cae = generate_invoice(parsed_data)
        CAE_response = convert_zeep_object_to_dict(returned_cae)

        return CAE_response
    else:
        
        logger.info("Checking if token is expired...")
        if is_token_expired():

            logger.info("Token expired.")
            request_access_token()
            returned_cae = generate_invoice(parsed_data)
            CAE_response = convert_zeep_object_to_dict(returned_cae)

            return CAE_response
        else:
            logger.info("Token not expired.")
            returned_cae = generate_invoice(parsed_data)
            CAE_response = convert_zeep_object_to_dict(returned_cae)

            return CAE_response

