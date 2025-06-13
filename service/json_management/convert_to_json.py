from zeep.helpers import serialize_object

from service.utils.logger import logger


def convert_zeep_object_to_dict(returned_cae: object) -> dict:

    """
    Zeep usually returns an object of type '<class 'zeep.objects.FECAEResponse'>'.
    To work with the CAE data, this object needs to be converted into a dictionary.
    This function performs that conversion and saves the data as a JSON file.
    """

    # Convert to dict/OrderedDict
    CAE_response = serialize_object(returned_cae)
    logger.debug("Zeep object converted to dict.")
    return CAE_response
