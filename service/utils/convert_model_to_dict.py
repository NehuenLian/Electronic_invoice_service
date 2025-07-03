# Convert pydantic model object to dict
from service.utils.logger import logger


def convert_pydantic_model_to_dict(sale_data: object) -> dict:
    
    parsed_data = sale_data.model_dump()
    return parsed_data