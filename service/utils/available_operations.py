from zeep import Client
from zeep.exceptions import Fault, TransportError


def list_afip_operations():
    """
    Lists the available operations and their input signatures
    from the AFIP SOAP service using Zeep.
    """
    afip_wsdl = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL"
    client = Client(wsdl=afip_wsdl)
    binding = client.service._binding  # Soap11Binding object
    for op_name, operation in binding._operations.items():
        print(f"Operation: {op_name}")
        print(operation.input.signature())


if __name__ == "__main__":
    list_afip_operations()
