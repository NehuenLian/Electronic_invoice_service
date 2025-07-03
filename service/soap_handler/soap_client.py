import logging
from builtins import ConnectionResetError
from service.soap_handler.analize_response import response_has_errors, find_error
from requests.exceptions import \
    ConnectionError  # Zeep uses requests behind it.
from service.utils.logger import logger
from tenacity import (before_sleep_log, retry, retry_if_exception_type,
                      stop_after_attempt, wait_fixed)
from zeep import Client
from zeep.exceptions import Fault, TransportError


# Implement retries with tenacity only for these Exceptions.
@retry(
        retry=retry_if_exception_type(( ConnectionResetError, ConnectionError, TransportError )),
        stop=stop_after_attempt(3),
        wait=wait_fixed(0.5),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
def login_cms(b64_cms: str) -> str:

    logger.info("Starting CMS login request to AFIP")
    afip_wsdl = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl"

    try:
        client = Client(wsdl=afip_wsdl)
        login_ticket_response = client.service.loginCms(b64_cms)
        logger.info("CMS login request to AFIP ended successfully.")

        if response_has_errors():
            find_error()
            
        return login_ticket_response

    except Fault as e:
        logger.debug(f"SOAP FAULT in login_cms: {e}")
        # TODO: This needs to be handled in a sophisticated way.  
        # Verify the presence of '"Errors": {"Err": [{...}]}' in the response.

    except Exception as e:
        logger.error(f"General exception in login_cms: {e}")
        raise


# Implement retries with tenacity only for these Exceptions.
@retry(
        retry=retry_if_exception_type(( ConnectionResetError, ConnectionError, TransportError )),
        stop=stop_after_attempt(3),
        wait=wait_fixed(0.5),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
def fecae_solicitar(full_built_invoice: dict) -> dict:

    logger.debug(f"full_built_invoice in fecae_solicitar: {full_built_invoice}")
    afip_wsdl = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL"

    try:
        client = Client(wsdl=afip_wsdl)
        response_cae = client.service.FECAESolicitar(full_built_invoice['Auth'], full_built_invoice['FeCAEReq'])

        if response_has_errors():
            find_error()

        return response_cae

    except Fault as e:
        logger.debug(f"SOAP FAULT in fecae_solicitar: {e}")
        # TODO: This needs to be handled in a sophisticated way.  
        # Verify the presence of '"Errors": {"Err": [{...}]}' in the response.

    except Exception as e:
        logger.error(f"General exception in fecae_solicitar: {e}")
        raise