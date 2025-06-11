from service.crypto.sign import get_binary_cms, sign_login_ticket_request
from service.payload_builder.builder import (add_auth_to_payload,
                                             build_afip_payload_from_sale,
                                             get_sale_json)
from service.soap_handler.soap_client import fecae_solicitar, login_cms
from service.time.time_management import compare_time
from service.utils.verify_timestamp import timestamp_exists
from service.xml_management.xml_builder import (
    build_login_ticket_request,
    extract_token_and_sign_from_loginticketresponse,
    parse_and_save_loginticketresponse, save_xml)
from service.utils.logger import logger


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

def generate_invoice():
    logger.info("Starting invoice generation process.")
    token, sign = extract_token_and_sign_from_loginticketresponse("loginTicketResponse.xml")
    logger.info("Token and sign successfully extracted from 'loginTicketResponse.xml'.")

    sale_data = get_sale_json()

    payload = build_afip_payload_from_sale(sale_data)
    full_built_invoice  = add_auth_to_payload(payload, token, sign)

    logger.info("Invoice payload built and signed successfully.")
    
    returned_invoice = fecae_solicitar(full_built_invoice)

    return returned_invoice

def main():
    logger.info("Checking if valid timestamp exists...")
    if not timestamp_exists():
        logger.info("Timestamp not found. Requesting new access token...")
        request_access_token()
        logger.info("Access token obtained. Proceeding to generate invoice...")
        generate_invoice()
        logger.info("Invoice generated and approved succesfully.")
    else:
        if compare_time():
            logger.info("Timestamp expired. Requesting new access token...")
            request_access_token()
            logger.info("Access token obtained. Proceeding to generate invoice...")
            generate_invoice()
            logger.info("Invoice generated and approved succesfully.")
        else:
            logger.info("Valid timestamp found. Proceeding to generate invoice...")
            generate_invoice()

    logger.info("Invoice generated and approved successfully.")

if __name__ == "__main__":
    main()