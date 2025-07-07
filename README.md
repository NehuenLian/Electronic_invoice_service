### Facturación Electrónica API - Argentina (AFIP/ARCA)
## Servicio Web de Facturación para Punto de Venta con Integración a la Agencia Tributaria Argentina

Este sistema es un servicio web que actúa como middleware entre sistemas POS locales y AFIP (Administración Federal de Ingresos Públicos) / ARCA (Agencia de Recaudación y Control Aduanero) (organismo fiscal de Argentina). Recibe comprobantes en formato JSON, los transforma a XML compatible con los Web Services de AFIP/ARCA, envía la solicitud vía SOAP, procesa la respuesta y devuelve el resultado al POS en formato JSON. También resuelve de forma automática ciertos errores comunes de facturación. El objetivo es simplificar el cumplimiento fiscal desde aplicaciones de escritorio.

## Stack tecnológico

- **Lenguaje:** Python  
- **Criptografía:** Uso directo de OpenSSL con `subprocess`  
- **Comunicación con AFIP:** XML + SOAP  
- **Comunicación con Punto de Venta:** FastAPI  
- **Deploy:** Docker (ideal)

## ¿Stateless?

Parcialmente. El servicio no almacena información transaccional ni de estado entre solicitudes, salvo por el token de autenticación que persiste en memoria durante 12 horas (hasta que se necesite generar otro) y se reutiliza para todas las facturas emitidas en ese período.

## Arquitectura y Estructura del Proyecto

La arquitectura está pensada para ser sencilla y práctica de entender: una carpeta por responsabilidad.  
A continuación se muestra un mapa ASCII de la arquitectura de carpetas y una breve descripción de la responsabilidad de cada una:

## Estructura del Proyecto

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

## Descripción de la arquitectura y los directorios

### `api/`
Contiene el endpoint POST que recibe los JSON con información de la venta y de la factura a construir antes de enviarla para su aprobación. También contiene los esquemas de Pydantic para la validación del JSON.

### `certificates/`
Contiene los certificados, claves privadas, CSRs y otros elementos criptográficos necesarios para firmar la solicitud del ticket de acceso.

### `controllers/`
Contiene controladores separados por servicio SOAP. Cada controlador maneja un servicio específico.

### `crypto/`
Contiene el módulo que firma la solicitud del ticket de acceso utilizando los elementos de la carpeta `certificates`.

### `payload_builder/`
Contiene el módulo que arma y manipula los diccionarios (`dict`) que necesita la librería Zeep para consumir los servicios SOAP.

### `error_handler/`
Contiene una función que recibe códigos de error y redirige el procesamiento a controladores especializados que intentan resolver dichos errores de forma automática. Este módulo puede ampliarse a medida que se descubren nuevos tipos de errores.

### `soap_management/`
Maneja la comunicación con los servicios SOAP de AFIP/ARCA y analiza las respuestas en busca de errores. Los errores suelen presentarse como un array al final de la respuesta.

### `time/`
Contiene funciones auxiliares para la gestión de fechas y horas.

### `utils/`
Contiene funciones auxiliares generales: logger, validación de existencia, entre otras.

### `xml_management/`
Almacena los archivos XML necesarios para el funcionamiento del servicio y contiene todas las funciones necesarias para construir y manipular estos archivos.

### `exceptions.py`
Contiene las excepciones personalizadas del servicio.

## Dependencias principales

- **lxml:** Biblioteca para el procesamiento de los XML, para manipular y validar los archivos XML requeridos por AFIP/ARCA.  
- **zeep:** Cliente SOAP para consumir los servicios web de AFIP/ARCA de forma sencilla.  
- **fastapi:** Para construir la API REST que recibe las solicitudes JSON desde el sistema POS.  
- **pydantic:** Validación y serialización de datos para que los JSON cumplan con los esquemas.  
- **tenacity:** Una de las ideas de este servicio es que logre generar la factura en la mayor cantidad posible de casos. En caso de errores no críticos, se realizan reintentos automáticos usando `tenacity`. Esta librería es ideal para eso.
- **ntplib:** Se utiliza en este caso para que la solicitud de ticket de acceso contenga la hora sincronizada con AFIP/ARCA. 

## Flujo de trabajo (simplificado)

1. Verificar si el archivo `loginTicketResponse.xml` existe:
   - Si existe, verificar si el token está expirado:
     - Si está expirado, generar un nuevo token desde cero.
     - Si no está expirado, reutilizar el token actual.
   - Si no existe, verificar si el archivo `loginTicketRequest.xml` existe:
     - Si existe, verificar si el campo `<expirationTime>` del token expiró:
       - Si expiró, generar un nuevo token desde cero.
       - Si no expiró, verificar si el token está expirado:
         - Si está expirado, generar un nuevo token desde cero.
         - Si no, generar el token a partir del existente.
     - Si no existe, generar un nuevo token desde cero.

2. Generar la factura (CAE) con el token válido obtenido o generado.

3. Devolver la respuesta con los datos del CAE.

## Ejecutar localmente sin Docker

1. Clonar el repositorio 
2. Instalar las dependencias: `pip install -r requirements.txt`
3. Levantar el servicio con Uvicorn:
- `uvicorn.service.api.app:app --reload`
4. Una vez disponible el servicio, podrá recibir un JSON con la estructura definida en `api/models/invoice.py` al endpoint que se encuentra en `api/app.py`.

## Ejemplo del JSON que espera recibir el endpoint

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

## Explicación de los servicios SOAP a consultar que se encuentran en este software  
Directorio: `service/soap_management/soap_client.py`

El archivo `soap_client.py` contiene las consultas a 3 de los servicios SOAP de AFIP/ARCA (el nombre de las funciones es el mismo que el del servicio consultado):

- `login_cms(b64ms)`  
  Servicio que permite obtener el ticket de acceso (TA) para autenticarse ante AFIP/ARCA.
  Recibe como parámetro un CMS (`b64ms`) que debe estar en binario (ver `crypto/sign.py/get_binary_cms()`).
  Devuelve un XML llamado `loginTicketResponse.xml` que contiene el token necesario para consultar los otros servicios, expira en 12 horas.

- `fecae_solicitar(full_built_invoice)`  
  Servicio que envía la solicitud de autorización para emitir el comprobante electrónico (factura).  
  Recibe un `dict` (se explica más adelante) con los datos de la factura, el token de acceso y la firma. Devuelve un CAE (Código de Autorización Electrónico) en forma de `OrderedDict`. Si la factura es aprobada, o, si hubo un error con los datos enviados, devuelve también un `OrderedDict` pero con un array adjunto al final con información del error.

- `fe_comp_ultimo_autorizado(auth, ptovta, cbtetipo)`  
  Este servicio consulta cuál fue el último comprobante autorizado por AFIP/ARCA para un determinado punto de venta (`ptovta`) y tipo de comprobante (`cbtetipo`).  
  Es fundamental para conocer el número correlativo que debe tener la próxima factura.  
  Recibe como argumento:
  
  - `auth`: Un `dict` que contiene las credenciales necesarias para la autenticación, incluyendo:
    - `token`: Token de acceso vigente.
    - `sign`: Firma digital.
    - `cuit`: CUIT de la empresa emisora.
  
  Este servicio se utiliza para solucionar el error `10016` (ver `service/response_errors_handler/error_handler.py`), solicitando el número de comprobante actual para agregarlo a la factura a aprobar luego de que se haya devuelto rechazada con dicho error adjunto.
---

### Ejemplo de la estructura de lo que debe recibir `fecae_solicitar(full_built_invoice)`:

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

### Ejemplo de respuesta exitosa:

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

### Ejemplo de respuesta con error:

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

## Licencia

Este proyecto está bajo la licencia [MIT](./LICENSE) (licencia permisiva de código abierto).

Resumen: Podés usar, copiar, modificar y distribuir el software libremente, siempre incluyendo el aviso de copyright y sin garantías.

---
