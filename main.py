from service.crypto.sign import get_binary_cms, sign_login_ticket_request
from service.payload_builder.builder import (add_auth_to_payload,
                                             build_afip_payload_from_sale,
                                             get_sale_json)
from service.soap_handler.soap_client import fecae_solicitar, login_cms
from service.time.time_management import compare_time
from service.utils import timestamp_exists
from service.xml_management.xml_builder import (
    build_login_ticket_request,
    extract_token_and_sign_from_loginticketresponse,
    parse_and_save_loginticketresponse, save_xml)


def request_access_token():
    root = build_login_ticket_request()
    save_xml(root, "loginTicketRequest.xml")
    sign_login_ticket_request()
    b64_cms = get_binary_cms()
    login_ticket_response = login_cms(b64_cms)
    parse_and_save_loginticketresponse(login_ticket_response)

def generate_invoice():
    token, sign = extract_token_and_sign_from_loginticketresponse("loginTicketResponse.xml")
    sale_data = get_sale_json()
    payload = build_afip_payload_from_sale(sale_data)
    full_built_invoice  = add_auth_to_payload(payload, token, sign)
    returned_invoice = fecae_solicitar(full_built_invoice)

    return returned_invoice

def main():

    if not timestamp_exists():
        # The timestamp does not exist, therefore neither does a token. Requesting access...
        request_access_token()
        # The token request was successfull, generating invoice...
        generate_invoice()
    else:
        if compare_time():
            # The timestamp exists but has expired. Requesting access for a new token...
            request_access_token()
            # The token request was successfull, generating invoice...
            generate_invoice()
        else:
            # Generating invoice...
            generate_invoice()

if __name__ == "__main__":
    main()