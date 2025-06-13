# Convert pydantic model object to dict
from service.utils.logger import logger


def convert_pydantic_model_to_dict(sale_data: object) -> dict:
    
    parsed_data = sale_data.model_dump()
    logger.debug("Pydantic model converted to dict.")

    return parsed_data