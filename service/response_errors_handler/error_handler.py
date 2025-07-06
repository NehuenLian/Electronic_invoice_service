from service.exceptions import NoErrorCodeFound
from service.response_errors_handler.sync_invoice_number_controller import \
    sync_invoice_number

# Dictionary of known errors.
# Format: {Error code: Solution}
errors_catalog = {
    10016 : sync_invoice_number,
}

def handle_error(error_code: int, parsed_data: dict):

    for error, handler in errors_catalog.items():
        if error_code == error:
            response = handler(parsed_data)

            return response

        else:
            raise NoErrorCodeFound("Error code not found in the error catalog.")