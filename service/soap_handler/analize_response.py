import json
from service.utils.logger import logger

# Dictionary of known errors.
# Format: {Error code: Error description}
errors_catalog = {
    10016 : "El numero o fecha del comprobante no se corresponde con el proximo a autorizar. Consultar metodo FECompUltimoAutorizado.",
}

# Handle if response_cae_dict its None too.
def response_has_errors(response_cae_dict: dict) -> bool:
    
    if response_cae_dict['Errors']:

        logger.info("Errors identified in the response.")
        return True
    
    else:
        logger.info("No errors in the response.")
        return False

def find_and_handle_error_code(response_cae_dict: dict):

    errors_level = response_cae_dict['Errors']

    err_level = errors_level['Err']

    error_code = err_level[0]['Code']
    error_message = err_level[0]['Msg']

    logger.debug(f'Error code: {error_code}')
    logger.debug(f'Error solution: {error_message}')

    for error, handler in errors_catalog.items():
        if error_code == error:
            print(handler)