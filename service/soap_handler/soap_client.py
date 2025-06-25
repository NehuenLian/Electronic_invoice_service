from zeep import Client
from zeep.exceptions import Fault

from service.exceptions import AlreadyValidAT
from service.utils.logger import logger


def login_cms(b64_cms: str) -> str:
    logger.info("Starting CMS login request to AFIP")
    afip_wsdl = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl"
    try:
        client = Client(wsdl=afip_wsdl)

        login_ticket_response = client.service.loginCms(b64_cms)
        return login_ticket_response
    
    except Fault as e:
        raise AlreadyValidAT(e)

def fecae_solicitar(full_built_invoice: dict) -> dict:
    logger.debug(f"full_built_invoice in fecae_solicitar: {full_built_invoice}")

    afip_wsdl = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL"
    client = Client(wsdl=afip_wsdl)
    response_cae = client.service.FECAESolicitar(full_built_invoice['Auth'], full_built_invoice['FeCAEReq'])

    return response_cae

