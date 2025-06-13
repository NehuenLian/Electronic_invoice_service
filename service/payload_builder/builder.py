import json

from service.utils.logger import logger


def add_auth_to_payload(token, sign):

    json_path = "service/json_management/sale_data.json"

    with open(json_path, 'r', encoding='utf-8') as file:
            sale_data = json.load(file)

    sale_data['Auth']['Token'] = token
    sale_data['Auth']['Sign'] = sign

    return sale_data