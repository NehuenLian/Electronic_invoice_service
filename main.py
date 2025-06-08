from service.crypto.sign import get_binary_cms, sign_login_ticket_request
from service.soap_handler.soap_client import login_cms
from service.time.time_management import compare_time
from service.utils import timestamp_exists
from service.xml_management.xml_builder import (build_login_ticket_request,
                                                save_xml)


def request_access_token():
    root = build_login_ticket_request()
    save_xml(root)
    sign_login_ticket_request()
    b64_cms = get_binary_cms()
    login_cms(b64_cms)

def main():

    if not timestamp_exists():
        # The timestamp does not exist, therefore neither does a token. Requesting access...
        request_access_token()
    else:
        if compare_time():
            # The timestamp exists but has expired. Requesting access for a new token...
            request_access_token()
        else:
            # Generating invoice...
            request_access_token()
            pass

if __name__ == "__main__":
    main()