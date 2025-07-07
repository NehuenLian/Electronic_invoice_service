# Flag to select WSAA environment:
# True = production, False = testing (homologation)
IS_WSAA_PRODUCTION = False

def get_login_cms_wsdl() -> str:
    if IS_WSAA_PRODUCTION:
        return "https://wsaa.afip.gov.ar/ws/services/LoginCms?WSDL"
    else:
        return "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?WSDL"


# Flag to select WSFE environment:
# True = production, False = testing (homologation)
IS_WSFE_PRODUCTION = False

def get_wsfe_wsdl() -> str:
    if IS_WSFE_PRODUCTION:
        return "https://servicios1.afip.gov.ar/wsfev1/service.asmx?WSDL"
    else:
        return "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL"
