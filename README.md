# Servicio Web de Facturación para Punto de Venta con Integración a la Agencia Tributaria Argentina

Este proyecto es un servicio web que actúa como middleware entre sistemas POS locales y AFIP/ARCA (organismos fiscales de Argentina). Recibe comprobantes en formato JSON, los transforma a XML compatible con los Web Services de AFIP/ARCA, envía la solicitud vía SOAP, procesa la respuesta y devuelve el resultado al POS en formato JSON. También resuelve de forma automática ciertos errores comunes de facturación. El objetivo es simplificar el cumplimiento fiscal desde aplicaciones de escritorio.

## Tech Stack

- **Lenguaje:** Python  
- **Criptografía:** Uso directo de OpenSSL con `subprocess`  
- **Comunicación con AFIP:** XML + SOAP  
- **Comunicación con Punto de Venta:** FastAPI  
- **Deploy:** Docker  

## ¿Stateless?

Parcialmente. El servicio no almacena información transaccional ni de estado entre solicitudes, salvo por el token de autenticación que persiste en memoria durante 12 horas (hasta que se necesite generar otro) y se reutiliza para todas las facturas emitidas en ese período.

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

## Flujo sugerido

1. Verificar si el token actual ha expirado (vigencia: 12h).
2. Si ha expirado, solicitar uno nuevo usando:
   - Clave privada (`.key`)
   - Certificado X.509 válido (vigencia: 2 años)
3. Generar el XML de la venta.
4. Firmar con OpenSSL(Comando de ejemplo):
   ```bash
   openssl cms -sign -in MiLoginTicketRequest.xml \
     -out MiLoginTicketRequest.xml.cms \
     -signer certificado_devuelto.pem \
     -inkey MiClavePrivada.key \
     -nodetach -outform PEM