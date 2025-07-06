from service.payload_builder.builder import add_auth_to_payload
from service.response_errors_handler.error_handler import handle_error
from service.soap_management.analize_response import (find_error_code,
                                                      response_has_errors)
from service.soap_management.soap_client import fecae_solicitar
from service.utils.convert_to_dict import convert_zeep_object_to_dict
from service.utils.logger import logger
from service.xml_management.xml_builder import extract_token_and_sign_from_xml


def generate_invoice(parsed_data: dict) -> dict:

    logger.info("Generating invoice...")
    token, sign = extract_token_and_sign_from_xml("loginTicketResponse.xml")
    full_built_invoice = add_auth_to_payload(parsed_data, token, sign)

    returned_cae = fecae_solicitar(full_built_invoice)

    logger.info("Verifying if the response has errors...")
    if response_has_errors(returned_cae):
        
        logger.info("Response has errors. Resolving...")
        error_code = find_error_code(returned_cae)
        updated_parsed_data = handle_error(error_code, parsed_data)
        logger.info("Error resolved. Retrying invoice submission")
        returned_cae = fecae_solicitar(updated_parsed_data)
    
    CAE_response = convert_zeep_object_to_dict(returned_cae)
    logger.info("Invoice generated.")

    return CAE_response 