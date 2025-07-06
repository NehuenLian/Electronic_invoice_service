from fastapi import FastAPI

from service.api.models.invoice import RootModel
from service.controllers.request_invoice_controller import \
    request_invoice_controller
from service.utils.convert_to_dict import convert_pydantic_model_to_dict
from service.utils.logger import logger

app = FastAPI()

@app.post("/invoice")
def generate_invoice(sale_data: RootModel) -> dict:
    
    logger.info("Invoice generation request received. Parsing input data and calling controller.")

    parsed_data = convert_pydantic_model_to_dict(sale_data)
    CAE_response = request_invoice_controller(parsed_data)

    return CAE_response