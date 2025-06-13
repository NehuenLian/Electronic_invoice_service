from service.crypto.sign import get_binary_cms, sign_login_ticket_request
from service.json_management.convert_to_json import convert_zeep_object_to_json, save_json
from service.payload_builder.builder import add_auth_to_payload
from service.soap_handler.soap_client import fecae_solicitar, login_cms
from service.time.time_management import is_token_expired
from service.utils.logger import logger
from service.utils.verify_timestamp import timestamp_exists
from service.xml_management.xml_builder import (
    build_login_ticket_request,
    extract_token_and_sign_from_loginticketresponse,
    parse_and_save_loginticketresponse, save_xml)


def request_access_token():
    logger.info("Starting access token request process.")

    root = build_login_ticket_request()
    logger.info("loginTicketRequest.xml generated successfully")

    save_xml(root, "loginTicketRequest.xml")
    sign_login_ticket_request()
    logger.info("CMS signature generated successfully.")

    b64_cms = get_binary_cms()
    login_ticket_response = login_cms(b64_cms)
    logger.info("loginTicketResponse received from ARCA.")

    parse_and_save_loginticketresponse(login_ticket_response)
    logger.info("loginTicketResponse parsed and saved successfully.")

def generate_invoice() -> object:
    logger.info("Starting invoice generation process.")
    token, sign = extract_token_and_sign_from_loginticketresponse("loginTicketResponse.xml")
    logger.info("Token and sign successfully extracted from 'loginTicketResponse.xml'.")

    full_built_invoice  = add_auth_to_payload(token, sign)

    logger.info("Invoice payload built and signed successfully.")
    
    returned_cae = fecae_solicitar(full_built_invoice)

    return returned_cae

def main():
    logger.info("Checking if valid timestamp exists...")
    if not timestamp_exists():
        logger.info("Timestamp not found. Requesting new access token...")
        request_access_token()
        logger.info("Access token obtained. Proceeding to generate invoice...")
        returned_cae = generate_invoice()
        json_file = convert_zeep_object_to_json(returned_cae)
        save_json(json_file, "CAE_response.json")
    else:
        if is_token_expired():
            logger.info("Timestamp expired. Requesting new access token...")
            request_access_token()
            logger.info("Access token obtained. Proceeding to generate invoice...")
            returned_cae = generate_invoice()
            json_file = convert_zeep_object_to_json(returned_cae)
            save_json(json_file, "CAE_response.json")
        else:
            logger.info("Valid timestamp found. Proceeding to generate invoice...")
            returned_cae = generate_invoice()
            json_file = convert_zeep_object_to_json(returned_cae)
            save_json(json_file, "CAE_response.json")

    logger.info("Invoice generated and approved successfully.")

if __name__ == "__main__":
    main()