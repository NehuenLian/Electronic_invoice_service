from service.utils.logger import logger


# Handle if response_cae_dict its None too.
def response_has_errors(response_cae_dict: dict) -> bool:
    
    if response_cae_dict['Errors']:

        logger.info("Errors identified in the response.")
        return True
    
    else:
        logger.info("No errors in the response.")
        return False

def find_error_code(response_cae_dict: dict) -> int:

    errors_level = response_cae_dict['Errors']

    err_level = errors_level['Err']

    error_code = err_level[0]['Code']
    error_message = err_level[0]['Msg']

    logger.debug(f'Error code: {error_code}')
    logger.debug(f'Error message: {error_message}')

    return error_code