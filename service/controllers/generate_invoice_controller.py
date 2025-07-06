from service.payload_builder.builder import add_auth_to_payload
from service.soap_handler.soap_client import fecae_solicitar
from service.utils.convert_to_dict import convert_zeep_object_to_dict
from service.utils.logger import logger
from service.xml_management.xml_builder import \
    extract_token_and_sign_from_loginticketresponse


def generate_invoice(parsed_data: dict) -> dict:

    logger.info("Generating invoice...")
    token, sign = extract_token_and_sign_from_loginticketresponse("loginTicketResponse.xml")
    full_built_invoice = add_auth_to_payload(parsed_data, token, sign)

    returned_cae = fecae_solicitar(full_built_invoice)
    CAE_response = convert_zeep_object_to_dict(returned_cae)
    logger.info("Invoice generated.")

    return CAE_response 