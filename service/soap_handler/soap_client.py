from zeep import Client

from service.utils.logger import logger


def login_cms(b64_cms: str) -> str:
    logger.info("Starting CMS login request to AFIP")
    afip_wsdl = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl"
    client = Client(wsdl=afip_wsdl)
    
    login_ticket_response = client.service.loginCms(b64_cms)
    logger.info("CMS login request completed successfully")

    return login_ticket_response


def fecae_solicitar(full_built_invoice: dict) -> dict:
    logger.debug(f"full_built_invoice in fecae_solicitar: {full_built_invoice}")
    logger.info("Sending FECAESolicitar request to AFIP")
    afip_wsdl = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL"

    client = Client(wsdl=afip_wsdl)

    response_cae = client.service.FECAESolicitar(full_built_invoice['Auth'], full_built_invoice['FeCAEReq'])
    logger.info("FECAESolicitar request completed")

    return response_cae
