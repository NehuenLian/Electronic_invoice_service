import json

from zeep.helpers import serialize_object


def convert_zeep_object_to_json(returned_cae: object) -> json:

    """
    Zeep usually returns an object of type '<class 'zeep.objects.FECAEResponse'>'.
    To work with the CAE data, this object needs to be converted into a dictionary.
    This function performs that conversion and saves the data as a JSON file.
    """

    # Convert to dict/OrderedDict
    dict_cae = serialize_object(returned_cae)

    # Convert to JSON
    json_cae = json.dumps(dict_cae, indent=2, ensure_ascii=False)

    return json_cae

def save_json(json_file: json, json_name: str):

    path = f"service/json_management/{json_name}"

    with open(path, 'w', encoding='utf-8') as new_json_file:
        new_json_file.write(json_file)