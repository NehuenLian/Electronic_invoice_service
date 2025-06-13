from service.utils.logger import logger


def add_auth_to_payload(sale_data: dict, token: str, sign: str) -> dict:
    
    sale_data['Auth']['Token'] = token
    sale_data['Auth']['Sign'] = sign
    logger.debug("Auth added to payload.")

    return sale_data
