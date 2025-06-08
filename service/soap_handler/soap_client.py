from lxml import etree
from requests import Session
from zeep import Client
from zeep.transports import Transport


def login_cms(b64_cms):
    afip_wsdl = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl"
    client = Client(wsdl=afip_wsdl)
    
    response = client.service.loginCms(b64_cms)

    print(response)