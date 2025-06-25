from service.cae_structure_management.convert_to_dict import \
    convert_zeep_object_to_dict
from service.crypto.sign import get_binary_cms, sign_login_ticket_request
from service.exceptions import AlreadyValidAT, loginTicketResponseNotFound
from service.payload_builder.builder import add_auth_to_payload
from service.soap_handler.soap_client import fecae_solicitar, login_cms
from service.time.time_management import is_token_expired
from service.utils.file_validations import (login_ticket_request_exists,
                                            login_ticket_response_exists)
from service.utils.logger import logger
from service.xml_management.xml_builder import (
    build_login_ticket_request,
    extract_token_and_sign_from_loginticketresponse,
    is_expiration_time_reached, parse_and_save_loginticketresponse, save_xml)


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

def generate_invoice(parsed_data: dict) -> dict:

    logger.info("Generating invoice...")
    token, sign = extract_token_and_sign_from_loginticketresponse("loginTicketResponse.xml")
    full_built_invoice = add_auth_to_payload(parsed_data, token, sign)
    returned_cae = fecae_solicitar(full_built_invoice)
    CAE_response = convert_zeep_object_to_dict(returned_cae)
    logger.info("Invoice generated.")

    return CAE_response 

def request_invoice_controller(parsed_data: dict) -> dict:

    # Main flow: validates the existence and validity of tickets and tokens to generate an AFIP/ARCA invoice

    logger.info("Starting the invoice request process...")
    logger.info("Checking if loginTicketResponse exists...")
    
    if login_ticket_response_exists():
        logger.info("loginTicketResponse exists.")
        logger.info("Checking if the token has expired...")
        if is_token_expired():
            logger.info("The token has expired")
            generate_token_from_scratch()
            CAE_response = generate_invoice(parsed_data)

        else:
            logger.info("The token is still valid")
            CAE_response = generate_invoice(parsed_data)
        
    else:
        logger.info("loginTicketResponse does not exist.")
        logger.info("Checking if loginTicketRequest exists...")
        if login_ticket_request_exists():
            logger.info("loginTicketRequest exists.")
            logger.info("Checking if the <expirationTime> of loginTicketRequest has expired...")
            if is_expiration_time_reached():

                logger.info("<expirationTime> has expired. Generating a new one...")
                generate_token_from_scratch()
                CAE_response = generate_invoice(parsed_data)

            else:
                logger.info("<expirationTime> is still valid.")
                logger.info("Checking if the token has expired...")
                if is_token_expired():
                    logger.info("The token has expired, generating a new one...")
                    generate_token_from_scratch()
                    CAE_response = generate_invoice(parsed_data)

                else:
                    generate_token_from_existing()
                    CAE_response = generate_invoice(parsed_data)

        else:
            logger.info("loginTicketRequest does not exist. It needs to be generated from scratch.")
            logger.info("Generating token (loginTicketResponse)...")
            generate_token_from_scratch()
            CAE_response = generate_invoice(parsed_data)
        
    return CAE_response
