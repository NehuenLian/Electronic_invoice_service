import logging
from builtins import ConnectionResetError
from typing import Optional

from requests.exceptions import \
    ConnectionError  # Zeep uses requests behind it.
from tenacity import (after_log, retry, retry_if_exception_type,
                      stop_after_attempt, wait_fixed)
from zeep import Client
from zeep.exceptions import Fault, TransportError

from service.utils.logger import logger
from service.utils.wsdl_manager import get_login_cms_wsdl, get_wsfe_wsdl


# Implement retries with tenacity only for these Exceptions.
@retry(
        retry=retry_if_exception_type(( ConnectionResetError, ConnectionError, TransportError )),
        stop=stop_after_attempt(3),
        wait=wait_fixed(0.5),
        before_sleep=after_log(logger.warning("Error in login_cms. Retrying..."), logging.WARNING),
    )
def login_cms(b64_cms: str) -> Optional[str]:

    logger.info("Starting CMS login request to AFIP")

    afip_wsdl = get_login_cms_wsdl()

    try:
        client = Client(wsdl=afip_wsdl)
        login_ticket_response = client.service.loginCms(b64_cms)
        logger.info("CMS login request to AFIP ended successfully.")
        
        logger.debug(f"login_ticket_response: {login_ticket_response}")
        return login_ticket_response

    except Fault as e:
        logger.debug(f"SOAP FAULT in login_cms: {e}")
        # TODO: This needs to be handled in a sophisticated way.  

    except Exception as e:
        logger.error(f"General exception in login_cms: {e}")
        raise


# Implement retries with tenacity only for these Exceptions.
@retry(
        retry=retry_if_exception_type(( ConnectionResetError, ConnectionError, TransportError )),
        stop=stop_after_attempt(3),
        wait=wait_fixed(0.5),
        before_sleep=after_log(logger.warning("Error in fecae_solicitar. Retrying..."), logging.WARNING),
    )
def fecae_solicitar(full_built_invoice: dict) -> Optional[dict]:

    logger.info(f"Generating invoice...")
    afip_wsdl = get_wsfe_wsdl()

    try:
        client = Client(wsdl=afip_wsdl)
        response_cae = client.service.FECAESolicitar(full_built_invoice['Auth'], full_built_invoice['FeCAEReq'])
        
        logger.debug(f"Response: {response_cae}")
        return response_cae

    except Fault as e:
        logger.debug(f"SOAP FAULT in fecae_solicitar: {e}")
        # TODO: This needs to be handled in a sophisticated way.  

    except Exception as e:
        logger.error(f"General exception in fecae_solicitar: {e}")
        raise


# Implement retries with tenacity only for these Exceptions.
@retry(
        retry=retry_if_exception_type(( ConnectionResetError, ConnectionError, TransportError )),
        stop=stop_after_attempt(3),
        wait=wait_fixed(0.5),
        before_sleep=after_log(logger.warning("Error in fe_comp_ultimo_autorizado. Retrying..."), logging.WARNING),
    )
def fe_comp_ultimo_autorizado(auth: dict, ptovta: int, cbtetipo: int) -> Optional[dict]:
    
    logger.info(f"Consulting last authorized invoice...")
    afip_wsdl = get_wsfe_wsdl()

    try:
        client = Client(wsdl=afip_wsdl)
        last_authorized_info = client.service.FECompUltimoAutorizado(auth, ptovta, cbtetipo)

        logger.debug(f"Response: {last_authorized_info}")

        return last_authorized_info

    except Fault as e:
        logger.debug(f"SOAP FAULT in fe_comp_ultimo_autorizado: {e}")
        # TODO: This needs to be handled in a sophisticated way.  

    except Exception as e:
        logger.error(f"General exception in fe_comp_ultimo_autorizado: {e}")
        raise