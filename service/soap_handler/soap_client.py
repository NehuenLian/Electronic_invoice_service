from requests.exceptions import \
    ConnectionError  # Zeep uses requests behind it.
from service.utils.logger import logger
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed, before_sleep
from zeep import Client
from zeep.exceptions import Fault, TransportError
from builtins import ConnectionResetError

def log_before_retry(retry_state):
    exc = retry_state.outcome.exception()
    logger.warning(f"Error {exc}, retrying...")

# Implement retries with tenacity only for these Exceptions.
@retry(
        retry=retry_if_exception_type(( ConnectionResetError, ConnectionError, TransportError )),
        stop=stop_after_attempt(3),
        wait=wait_fixed(0.5),
        before_sleep=log_before_retry,
    )
def login_cms(b64_cms: str) -> str:

    logger.info("Starting CMS login request to AFIP")
    afip_wsdl = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl"

    try:
        client = Client(wsdl=afip_wsdl)
        login_ticket_response = client.service.loginCms(b64_cms)

        return login_ticket_response

    except Fault as e:
        logger.debug(f"SOAP FAULT in login_cms: {e}")
        # TODO: This needs to be handled in a sofisticate way. Verify the ['Errors'] array in the response
    
    except Exception as e:
        logger.error(f"General exception in login_cms: {e}")
        raise


# Implement retries with tenacity only for these Exceptions.
@retry(
        retry=retry_if_exception_type(( ConnectionResetError, ConnectionError, TransportError )),
        stop=stop_after_attempt(3),
        wait=wait_fixed(0.5),
        before_sleep=log_before_retry,
    )
def fecae_solicitar(full_built_invoice: dict) -> dict:

    logger.debug(f"full_built_invoice in fecae_solicitar: {full_built_invoice}")
    afip_wsdl = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL"

    try:
        client = Client(wsdl=afip_wsdl)
        response_cae = client.service.FECAESolicitar(full_built_invoice['Auth'], full_built_invoice['FeCAEReq'])

        return response_cae

    except Fault as e:
        logger.debug(f"SOAP FAULT in fecae_solicitar: {e}")
        # TODO: This needs to be handled in a sofisticate way. Verify the ['Errors'] array in the response
    
    except Exception as e:
        logger.error(f"General exception in fecae_solicitar: {e}")
        raise