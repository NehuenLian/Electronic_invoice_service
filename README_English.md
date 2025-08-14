# Web Invoicing Service for Point of Sale with Integration to the Argentine Tax Agency

This system is a web service that acts as middleware between local POS systems and AFIP (Administración Federal de Ingresos Públicos) / ARCA (Customs Revenue and Control Agency), the tax authority in Argentina. It receives invoices in JSON format, transforms them into XML compatible with AFIP/ARCA Web Services, sends the request via SOAP, processes the response, and returns the result to the POS in JSON format. It also automatically handles certain common invoicing errors. The goal is to simplify tax compliance from desktop applications.

[![Python](https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![lxml](https://img.shields.io/badge/lxml-5.4.0-orange)](https://pypi.org/project/lxml/)
[![zeep](https://img.shields.io/badge/zeep-4.3.1-green)](https://pypi.org/project/zeep/)
[![fastapi](https://img.shields.io/badge/fastapi-0.115.12-blueviolet)](https://fastapi.tiangolo.com/)
[![pydantic](https://img.shields.io/badge/pydantic-2.11.5-red)](https://pypi.org/project/pydantic/)
[![tenacity](https://img.shields.io/badge/tenacity-9.1.2-yellow)](https://pypi.org/project/tenacity/)
[![ntplib](https://img.shields.io/badge/ntplib-0.4.0-lightgrey)](https://pypi.org/project/ntplib/)

## Tech Stack

- **Language:** Python  
- **Cryptography:** Direct use of OpenSSL with `subprocess`  
- **Communication with AFIP:** XML + SOAP  
- **Communication with Point of Sale:** FastAPI  
- **Deployment:** Docker (ideal)

## Stateless?

Partially. The service does not store transactional or state information between requests, except for the authentication token which persists in memory for 12 hours (until it needs to be refreshed) and is reused for all invoices issued within that period.

## Project Architecture and Structure

The architecture is designed to be simple and easy to understand: one folder per responsibility.  
Below is an ASCII map of the folder structure and a brief description of each one's responsibility:

## Project Structure

```text
INVOICE_SERVICE  
├── service  
│   ├── api/ 
│   ├── certificates/
│   ├── controllers/
│   ├── crypto/
│   ├── payload_builder/
│   ├── error_handler/
│   ├── soap_management/
│   ├── time/
│   ├── utils/
│   └── xml_management/
├── exceptions.py  
├── .gitignore  
├── main.py  
├── README_English.md  
├── README.md  
└── requirements.txt
```

## Architecture and Directory Description

### `api/`
Contains the POST endpoint that receives the JSON with sales and invoice information to be built before sending it for approval. It also contains the Pydantic schemas for JSON validation.

### `certificates/`
Stores certificates, private keys, CSRs, and other cryptographic elements needed to sign the access ticket request.

### `controllers/`
Contains controllers separated by SOAP service. Each controller handles a specific service.

### `crypto/`
Contains the module that signs the access ticket request using the elements from the `certificates` folder.

### `payload_builder/`
Contains the module that builds and manipulates the dictionaries (`dict`) required by the Zeep library to consume SOAP services.

### `error_handler/`
Contains a function that receives error codes and redirects processing to specialized controllers that attempt to automatically resolve those errors. This module can be expanded as new error types are discovered.

### `soap_management/`
Handles communication with AFIP/ARCA SOAP services and parses the responses looking for errors. Errors usually appear as an array at the end of the response.

### `time/`
Contains helper functions for date and time management.

### `utils/`
Contains general helper functions: logger, existence validation, among others.

### `xml_management/`
Stores the XML files required for the service to function and contains all necessary functions to build and manipulate these files.

### `exceptions.py`
Contains the custom exceptions of the service.

## Main Dependencies

- **lxml:** Library for XML processing, used to manipulate and validate the XML files required by AFIP/ARCA.  
- **zeep:** SOAP client for easily consuming AFIP/ARCA web services.  
- **fastapi:** Used to build the REST API that receives JSON requests from the POS system.  
- **pydantic:** Data validation and serialization to ensure that the JSONs comply with the schemas.  
- **tenacity:** One of the goals of this service is to generate invoices in as many cases as possible. In the case of non-critical errors, automatic retries are performed using `tenacity`. This library is ideal for that purpose.
- **ntplib:** Used to ensure that the access ticket request contains the time synchronized with AFIP/ARCA.

## Workflow (Simplified)

1. Check if the file `loginTicketResponse.xml` exists:
   - If it exists, verify if the token is expired:
     - If expired, generate a new token from scratch.
     - If not expired, reuse the current token.
   - If it does not exist, check if the file `loginTicketRequest.xml` exists:
     - If it exists, check if the `<expirationTime>` field in the token has expired:
       - If expired, generate a new token from scratch.
       - If not expired, verify if the token is expired:
         - If expired, generate a new token from scratch.
         - If not, generate the token from the existing one.
     - If it does not exist, generate a new token from scratch.

2. Generate the invoice (CAE) using the valid token obtained or generated.

3. Return the response with the CAE data.

## Running Locally Without Docker

1. Clone the repository  
2. Install dependencies: `pip install -r requirements.txt`  
3. Start the service with Uvicorn:  
   - `uvicorn.service.api.app:app --reload`  
4. Once the service is running, it will accept a JSON with the structure defined in `api/models/invoice.py` at the endpoint located in `api/app.py`.

## Example of the JSON Expected by the Endpoint

```json
{
    "Auth": {
        "Cuit": 20123456789
    },
    "FeCAEReq": {
        "FeCabReq": {
            "CantReg": 1,
            "PtoVta": 1,
            "CbteTipo": 6
        },
        "FeDetReq": {
            "FECAEDetRequest": {
                "Concepto": 1,
                "DocTipo": 96,
                "DocNro": 12345678,
                "CbteDesde": 1,
                "CbteHasta": 1,
                "CbteFch": "20250705",
                "ImpTotal": 1210.00,
                "ImpTotConc": 0.00,
                "ImpNeto": 1000.00,
                "ImpOpEx": 0.00,
                "ImpTrib": 0.00,
                "ImpIVA": 210.00,
                "MonId": "PES",
                "MonCotiz": 1.00,
                "CondicionIVAReceptorId": 5,
                "Iva": {
                    "AlicIva": {
                        "Id": 5,
                        "BaseImp": 1000.00,
                        "Importe": 210.00
                    }
                }
            }
        }
    }
}
```

## Explanation of the SOAP Services Queried by This Software  
Directory: `service/soap_management/soap_client.py`

The file `soap_client.py` contains calls to 3 of the AFIP/ARCA SOAP services (the function names match the service names):

- `login_cms(b64ms)`  
  Service that obtains the access ticket (TA) to authenticate with AFIP/ARCA.  
  It receives a CMS (`b64ms`) parameter, which must be in binary (see `crypto/sign.py/get_binary_cms()`).  
  Returns an XML called `loginTicketResponse.xml` containing the token needed to query other services, which expires in 12 hours.

- `fecae_solicitar(full_built_invoice)`  
  Service that sends the authorization request to issue the electronic invoice.  
  Receives a `dict` (explained later) with invoice data, access token, and signature. Returns a CAE (Electronic Authorization Code) as an `OrderedDict`. If the invoice is approved, or if there was an error with the sent data, it also returns an `OrderedDict` but with an array attached at the end containing error information.

- `fe_comp_ultimo_autorizado(auth, ptovta, cbtetipo)`  
  This service queries the last invoice authorized by AFIP/ARCA for a given point of sale (`ptovta`) and invoice type (`cbtetipo`).  
  It is essential to know the next invoice’s sequential number.  
  Receives as argument:
  
  - `auth`: A `dict` containing the credentials needed for authentication, including:
    - `token`: Current access token.
    - `sign`: Digital signature.
    - `cuit`: CUIT of the issuing company.
  
  This service is used to resolve error `10016` (see `service/response_errors_handler/error_handler.py`), by requesting the current invoice number to add it to the invoice to be approved after it was rejected with this error attached.

---

## Additional Considerations

- **Access Ticket Persistence:**  
  If the container or server where the service is deployed goes down, there is no issue with the access tickets (`loginTicketResponse.xml`). Upon restarting and receiving an invoicing request, the service will detect that the files are missing and automatically generate a new ticket.

- **Flexible Deployment:**  
  Using Docker is not mandatory. The service can run directly as a script or within any Python environment, as long as the input and output file formats are respected. The protection of credentials (tokens, certificates) is the responsibility of the user or environment administrator.

### Full Lifecycle Flow Represented with Logs (Including Automatic Error Correction)

```
2025-08-14 15:17:36,584 - INFO - Starting the invoice request process...
2025-08-14 15:17:36,584 - INFO - Checking if loginTicketResponse exists...
2025-08-14 15:17:36,584 - INFO - loginTicketResponse exists.
2025-08-14 15:17:36,584 - INFO - Checking if the token has expired...
2025-08-14 15:17:36,584 - DEBUG - Running is_expired() function for loginTicketRequest.xml
2025-08-14 15:17:36,584 - DEBUG - Consulting NTP for get the datetime...
2025-08-14 15:17:36,622 - DEBUG - Datetime values: epoch: 1755195434 | gentime: 2025-08-14T18:17:14Z | exptime: 2025-08-14T18:27:14Z
2025-08-14 15:17:36,627 - INFO - The token has expired
2025-08-14 15:17:36,627 - DEBUG - Consulting NTP for get the datetime...
2025-08-14 15:17:36,649 - DEBUG - Datetime values: epoch: 1755195434 | gentime: 2025-08-14T18:17:14Z | exptime: 2025-08-14T18:27:14Z
2025-08-14 15:17:36,650 - INFO - loginTicketRequest.xml successfully saved.
2025-08-14 15:17:36,650 - DEBUG - Signing loginTicketRequest.xml...
2025-08-14 15:17:36,691 - DEBUG - loginTicketRequest.xml successfully signed.
2025-08-14 15:17:36,691 - INFO - Starting CMS login request to AFIP
2025-08-14 15:17:36,889 - INFO - CMS login request to AFIP ended successfully.
2025-08-14 15:17:36,889 - DEBUG - login_ticket_response: <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<loginTicketResponse version="1.0">
    <header>
        <source>CN=wsaahomo, O=AFIP, C=AR, SERIALNUMBER=CUIT 44352675245</source>
        <destination>SERIALNUMBER=CUIT 20123456789, CN=certificadodefinitivo</destination>
        <uniqueId>3359896406</uniqueId>
        <generationTime>2025-08-14T15:17:14.429-03:00</generationTime>
        <expirationTime>2025-08-15T03:17:14.429-03:00</expirationTime>
    </header>
    <credentials>
        <token>P...g==</token>
        <sign>H...w=</sign>
    </credentials>
</loginTicketResponse>

2025-08-14 15:17:36,890 - INFO - loginTicketResponse.xml successfully saved.
2025-08-14 15:17:36,890 - INFO - Token generated.
2025-08-14 15:17:36,890 - INFO - Generating invoice...
2025-08-14 15:17:36,890 - DEBUG - Auth added to payload.
2025-08-14 15:17:36,890 - INFO - Generating invoice...
2025-08-14 15:17:37,215 - DEBUG - Response: {
    'FeCabResp': {
        'Cuit': 20123456789,
        'PtoVta': 1,
        'CbteTipo': 6,
        'FchProceso': '20250814151718',
        'CantReg': 1,
        'Resultado': 'R',
        'Reproceso': 'N'
    },
    'FeDetResp': {
        'FECAEDetResponse': [
            {
                'Concepto': 1,
                'DocTipo': 96,
                'DocNro': 12345678,
                'CbteDesde': 69,
                'CbteHasta': 69,
                'CbteFch': '20250728',
                'Resultado': 'R',
                'Observaciones': None,
                'CAE': None,
                'CAEFchVto': None
            }
        ]
    },
    'Events': None,
    'Errors': {
        'Err': [
            {
                'Code': 10016,
                'Msg': 'El numero o fecha del comprobante no se corresponde con el proximo a autorizar. Consultar metodo FECompUltimoAutorizado.'
            }
        ]
    }
}
2025-08-14 15:17:37,216 - INFO - Verifying if the response has errors...
2025-08-14 15:17:37,216 - INFO - Errors identified in the response.
2025-08-14 15:17:37,216 - INFO - Response has errors. Resolving...
2025-08-14 15:17:37,217 - DEBUG - Error code: 10016
2025-08-14 15:17:37,217 - DEBUG - Error message: El numero o fecha del comprobante no se corresponde con el proximo a autorizar. Consultar metodo FECompUltimoAutorizado.
2025-08-14 15:17:37,217 - INFO - Starting invoice number synchronization.
2025-08-14 15:17:37,217 - INFO - Consulting last authorized invoice...
2025-08-14 15:17:37,458 - DEBUG - Response: {
    'PtoVta': 1,
    'CbteTipo': 6,
    'CbteNro': 83,
    'Errors': None,
    'Events': None
}
2025-08-14 15:17:37,459 - INFO - Updated invoice with new number: 84
2025-08-14 15:17:37,459 - INFO - Error resolved. Retrying invoice submission
2025-08-14 15:17:37,459 - INFO - Generating invoice...
2025-08-14 15:17:37,821 - DEBUG - Response: {
    'FeCabResp': {
        'Cuit': 20123456789,
        'PtoVta': 1,
        'CbteTipo': 6,
        'FchProceso': '20250814151715',
        'CantReg': 1,
        'Resultado': 'R',
        'Reproceso': 'N'
    },
    'FeDetResp': {
        'FECAEDetResponse': [
            {
                'Concepto': 1,
                'DocTipo': 96,
                'DocNro': 12345678,
                'CbteDesde': 84,
                'CbteHasta': 84,
                'CbteFch': '20250728',
                'Resultado': 'R',
                'Observaciones': {
                    'Obs': [
                        {
                            'Code': 10016,
                            'Msg': 'Campo CbteFch Debe estar comprendido  en el  rango  N-5 y N+5 siendo N la fecha de envio del pedido  de autorizacion para 1 - Productos'
                        }
                    ]
                },
                'CAE': None,
                'CAEFchVto': None
            }
        ]
    },
    'Events': None,
    'Errors': None
}
2025-08-14 15:17:37,822 - DEBUG - Zeep object converted to dict.
2025-08-14 15:17:37,822 - INFO - Invoice generated.
```

---

### Example of the structure that `fecae_solicitar(full_built_invoice)` should receive:

```text
{
  "Auth": {
    "Cuit": 20123456789,
    "Token": "PD94...28+Cg==",
    "Sign": "ikM/Ut...wFwvk="
  },
  "FeCAEReq": {
    "FeCabReq": {
      "CantReg": 1,
      "PtoVta": 1,
      "CbteTipo": 6
    },
    "FeDetReq": {
      "FECAEDetRequest": {
        "Concepto": 1,
        "DocTipo": 96,
        "DocNro": 12345678,
        "CbteDesde": 69,
        "CbteHasta": 69,
        "CbteFch": "20250705",
        "ImpTotal": 1210.0,
        "ImpTotConc": 0.0,
        "ImpNeto": 1000.0,
        "ImpOpEx": 0.0,
        "ImpTrib": 0.0,
        "ImpIVA": 210.0,
        "MonId": "PES",
        "MonCotiz": 1.0,
        "CondicionIVAReceptorId": 5,
        "Iva": {
          "AlicIva": {
            "Id": 5,
            "BaseImp": 1000.0,
            "Importe": 210.0
          }
        }
      }
    }
  }
}
```

### Example of a successful response:

```text
{
    'FeCabResp': {
        'Cuit': 20123456789,
        'PtoVta': 1,
        'CbteTipo': 6,
        'FchProceso': '20250706220036',
        'CantReg': 1,
        'Resultado': 'A',
        'Reproceso': 'N'
    },
    'FeDetResp': {
        'FECAEDetResponse': [
            {
                'Concepto': 1,
                'DocTipo': 96,
                'DocNro': 12345678,
                'CbteDesde': 76,
                'CbteHasta': 76,
                'CbteFch': '20250705',
                'Resultado': 'A',
                'Observaciones': None,
                'CAE': '75272259316252',
                'CAEFchVto': '20250715'
            }
        ]
    },
    'Events': None,
    'Errors': None
}
```

### Example of an error response:

```text
{
    'FeCabResp': {
        'Cuit': 20123456789,
        'PtoVta': 1,
        'CbteTipo': 6,
        'FchProceso': '20250706215928',
        'CantReg': 1,
        'Resultado': 'R',
        'Reproceso': 'N'
    },
    'FeDetResp': {
        'FECAEDetResponse': [
            {
                'Concepto': 1,
                'DocTipo': 96,
                'DocNro': 12345678,
                'CbteDesde': 69,
                'CbteHasta': 69,
                'CbteFch': '20250705',
                'Resultado': 'R',
                'Observaciones': None,
                'CAE': None,
                'CAEFchVto': None
            }
        ]
    },
    'Events': None,
    'Errors': {
        'Err': [
            {
                'Code': 10016,
                'Msg': 'El numero o fecha del comprobante no se corresponde con el proximo a autorizar. Consultar metodo FECompUltimoAutorizado.'
            }
        ]
    }
}
```

## License

This project is licensed under the [MIT](./LICENSE) license (a permissive open-source license).

You are free to use, copy, modify, and distribute the software, always including the copyright notice and without any warranties.

---
