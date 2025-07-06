from service.controllers.generate_invoice_controller import generate_invoice
from service.controllers.request_access_token_controller import (
    generate_token_from_existing, generate_token_from_scratch)
from service.utils.file_validations import xml_exists
from service.utils.logger import logger
from service.xml_management.xml_builder import is_expired


def request_invoice_controller(parsed_data: dict) -> dict:

    # Main flow: validates the existence and validity of tickets and tokens to generate an AFIP/ARCA invoice

    logger.info("Starting the invoice request process...")
    logger.info("Checking if loginTicketResponse exists...")
    
    if xml_exists("loginTicketResponse.xml"):
        logger.info("loginTicketResponse exists.")
        logger.info("Checking if the token has expired...")
        is_token_expired = is_expired("loginTicketRequest.xml")

        if is_token_expired:
            logger.info("The token has expired")
            generate_token_from_scratch()
            CAE_response = generate_invoice(parsed_data)
        
        else:
            logger.info("The token is valid")
            CAE_response = generate_invoice(parsed_data)
        
    else:
        logger.info("loginTicketResponse does not exist.")
        logger.info("Checking if loginTicketRequest exists...")

        if xml_exists("loginTicketRequest.xml"):

            logger.info("loginTicketRequest exists.")
            logger.info("Checking if the <expirationTime> of loginTicketRequest has expired...")
            is_expiration_time_reached = is_expired("loginTicketRequest.xml")
            if is_expiration_time_reached:

                logger.info("<expirationTime> has expired. Generating a new one...")
                generate_token_from_scratch()
                CAE_response = generate_invoice(parsed_data)

            else:
                logger.info("<expirationTime> is still valid.")

                logger.info("Checking if the token has expired...")
                is_token_expired = is_expired("loginTicketRequest.xml")
                if is_token_expired:

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
