import os


def get_sale_json() -> dict:
    # Gets the json with the sale summary and turns it in a dict
    pass

def build_afip_payload_from_sale(sale_data: dict) -> dict:

    sale_data = { # Hardcoded dict for testing. Example data
        'Auth': {
            'Token': "",
            'Sign': "",
            'Cuit': "",
        },
        'FeCAEReq': {
            'FeCabReq': {
                'CantReg': 1,
                'PtoVta': 1,
                'CbteTipo': 6,
            },
            'FeDetReq': {
                'FECAEDetRequest': {
                    'Concepto': 1,
                    'DocTipo': 96,
                    'DocNro': 12345678,
                    'CbteDesde': 8,
                    'CbteHasta': 8,
                    'CbteFch': '20250603',
                    'ImpTotal': 1210.00,
                    'ImpTotConc': 0.00,
                    'ImpNeto': 1000.00,
                    'ImpOpEx': 0.00,
                    'ImpTrib': 0.00,
                    'ImpIVA': 210.00,
                    'MonId': 'PES',
                    'MonCotiz': 1.00,
                    'CondicionIVAReceptorId': 5,
                    'Iva': {
                        'AlicIva': {
                            'Id': 5,
                            'BaseImp': 1000.00,
                            'Importe': 210.00,
                        }
                    }
                }
            }
        }
    }

    return sale_data

def add_auth_to_payload(payload: dict, token: str, sign: str) -> dict:

    payload["Auth"] = {
        'Token' : token,
        'Sign' : sign,
        'Cuit' : int(os.getenv("PERSON_CUIT"))
        }
    
    return payload
