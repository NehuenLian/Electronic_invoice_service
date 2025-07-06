from service.utils.logger import logger


def add_auth_to_payload(sale_data: dict, token: str, sign: str) -> dict:
    
    sale_data['Auth']['Token'] = token
    sale_data['Auth']['Sign'] = sign
    logger.debug("Auth added to payload.")

    return sale_data

def extract_ptovta_and_cbtetipo(parsed_data: dict) -> tuple[int, str, str]:
    cuit = int(parsed_data["Auth"]["Cuit"])
    ptovta = int(parsed_data["FeCAEReq"]["FeCabReq"]["PtoVta"])
    cbtetipo = int(parsed_data["FeCAEReq"]["FeCabReq"]["CbteTipo"])

    return cuit, ptovta, cbtetipo

def build_auth(token: str, sign: str, cuit: int) -> dict:

    auth = {
        "Token" : token,
        "Sign" : sign,
        "Cuit" : cuit,
    }

    return auth

def extract_cbtenro(last_authorized_info: dict) -> int:
    """
    last_authorized_info structure:

    last_authorized_info = {
        'PtoVta': 1,
        'CbteTipo': 6,
        'CbteNro': 69,
        'Errors': None,
        'Events': None
    }

    """
    cbte_nro =  last_authorized_info['CbteNro']
    return cbte_nro

def update_sale_data(parsed_data: dict, cbte_nro: int) -> dict:

    parsed_data['FeCAEReq']['FeDetReq']['FECAEDetRequest']['CbteDesde'] = cbte_nro + 1
    parsed_data['FeCAEReq']['FeDetReq']['FECAEDetRequest']['CbteHasta'] = cbte_nro + 1
    
    updated_invoice = parsed_data

    return updated_invoice
