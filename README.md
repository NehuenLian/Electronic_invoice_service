# Proyecto: API de facturación para POS con integración AFIP

## Descripción del proyecto

Este proyecto es un servicio web que actúa como middleware entre sistemas POS locales y la AFIP/ARCA. Recibe comprobantes en formato JSON, los transforma a XML compatible con el WS de AFIP/ARCA, envía la solicitud vía SOAP, procesa la respuesta y la devuelve al POS en JSON. Automatiza la generación de tickets impresos y PDFs, simplificando el cumplimiento fiscal desde aplicaciones de escritorio.

---

## Objetivo General

Implementar un servicio web, creado desde cero en Python, que realice tareas criptográficas y se comunique con el servicio web de la entidad tributaria (ARCA) para emitir tickets fiscales al consumidor final, cumpliendo con las normativas vigentes de facturación electrónica.

---

## Objetivos específicos

- Automatizar la solicitud de token para autenticación.
- Implementar correctamente los algoritmos criptográficos requeridos.
- Firmar y enviar comprobantes electrónicos.
- Validar la respuesta del servicio tributario y almacenar la información útil.

---

## Requerimientos funcionales

1. El servicio debe verificar si el **token** vigente ha expirado antes de enviar una factura.
2. Debe implementar **todos los procesos criptográficos requeridos por ARCA** usando claves, certificados y firmas digitales.

---

## Requerimientos no funcionales

1. El código fuente debe ser modular y fácilmente modificable, sin comprometer el despliegue.

---

## Tecnologías a utilizar

- **Lenguaje principal:** Python  
- **Criptografía:** Uso directo de `openssl` mediante `subprocess`  
- **Comunicación:** XML + SOAP

---

## Plan de trabajo

1. **Investigación**  
   Lectura detallada de la documentación oficial de ARCA sobre criptografía, autenticación y envío de comprobantes.

2. **Pruebas manuales en entorno sandbox**  
   Ejecutar procesos manuales para verificar comprensión y funcionamiento del entorno.

3. **Pruebas finales**  
   Validación del script completo: firma, autenticación, envío, y recepción del XML aprobado.

---

## Criterios de éxito

1. El servicio es capaz de **firmar**, **enviar** un comprobante XML válido, y recibir una **respuesta aprobada** del servicio tributario, indicando que el comprobante fue aceptado.

---

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