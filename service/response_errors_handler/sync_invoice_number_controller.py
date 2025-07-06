from service.payload_builder.builder import (build_auth, extract_cbtenro,
                                             extract_ptovta_and_cbtetipo,
                                             update_sale_data)
from service.soap_management.soap_client import fe_comp_ultimo_autorizado
from service.utils.logger import logger
from service.xml_management.xml_builder import extract_token_and_sign_from_xml


def sync_invoice_number(parsed_data: dict):
    logger.info("Starting invoice number synchronization.")

    token, sign = extract_token_and_sign_from_xml("loginTicketResponse.xml")
    cuit, ptovta, cbtetipo = extract_ptovta_and_cbtetipo(parsed_data)
    auth = build_auth(token, sign, cuit)

    last_authorized_info = fe_comp_ultimo_autorizado(auth, ptovta, cbtetipo)
    cbte_nro = extract_cbtenro(last_authorized_info)
    updated_invoice = update_sale_data(parsed_data, cbte_nro)
    logger.info(f"Updated invoice with new number: {cbte_nro + 1}")
    
    return updated_invoice