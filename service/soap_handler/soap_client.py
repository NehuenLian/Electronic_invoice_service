from lxml import etree
from requests import Session
from zeep import Client
from zeep.transports import Transport


def login_cms(b64_cms: str) -> str:
    afip_wsdl = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl"
    client = Client(wsdl=afip_wsdl)
    
    login_ticket_response = client.service.loginCms(b64_cms)

    return login_ticket_response

def fecae_solicitar(full_built_invoice: dict) -> dict:

    afip_wsdl = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL"

    client = Client(wsdl=afip_wsdl)

    response = client.service.FECAESolicitar(full_built_invoice ['Auth'], full_built_invoice ['FeCAEReq'])

    print(response)
    print(type(response))
    return response