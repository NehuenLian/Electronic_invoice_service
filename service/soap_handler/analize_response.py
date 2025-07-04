import json
from service.utils.logger import logger


# Dictionary of known errors.
# Format: {Error code: Error description}
errors = {
    10016 : "El numero o fecha del comprobante no se corresponde con el proximo a autorizar. Consultar metodo FECompUltimoAutorizado.",
}

# Manejar si es none tambien
def response_has_errors() -> bool:

    with open("CAE_response.json", "r", encoding="utf-8") as file:
        response_json = file.read()
    
    response_json_dict = json.loads(response_json)
    
    if response_json_dict['Errors']:
        print(f"AAAAAAAA {response_json_dict['Errors']}")
        logger.info("Errors identified in the response.")
        return True
    
    else:
        logger.info("No errors in the response.")
        return False

def find_error():

    with open("CAE_response.json", "r", encoding="utf-8") as file:
        response_json = file.read()

    response_json_dict = json.loads(response_json)

    errors_level = response_json_dict['Errors']

    err_level = errors_level['Err']

    error_code = err_level[0]['Code']
    error_message = err_level[0]['Msg']

    print(f'Error code: {error_code}')
    print(f'Error message: {error_message}')
