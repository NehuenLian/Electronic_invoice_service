# Invoicing API for POS with Integration to the Argentine Tax Agency

## Project Description

This project is a web service that acts as middleware between local POS systems and the Argentine tax agency. It receives invoices in JSON format, transforms them into XML compatible with the agency’s web services, sends the request via SOAP, processes the response, and returns it to the POS in JSON format. It automates ticket printing and PDF generation, simplifying tax compliance for desktop applications.

---

## General Objective

Implement a web service, built from scratch in Python, that performs cryptographic tasks and communicates with the tax authority’s web service (ARCA) to issue fiscal tickets to the final consumer, complying with current electronic invoicing regulations.

---

## Specific Objectives

- Automate the token request for authentication.
- Correctly implement the cryptographic algorithms required.
- Sign and send electronic invoices.
- Validate the tax service’s response and store useful information.

---

## Functional Requirements

1. The service must verify if the current **token** has expired before sending an invoice.
2. It must implement **all cryptographic processes required by ARCA** using keys, certificates, and digital signatures.

---

## Non-functional Requirements

1. The source code must be modular and easily maintainable, without compromising deployment.

---

## Technologies to Use

- **Main language:** Python  
- **Cryptography:** direct use of `openssl` via `subprocess`  
- **Communication:** XML + SOAP  

---

## Work Plan

1. **Research**  
   Detailed reading of ARCA’s official documentation about cryptography, authentication, and invoice submission.

2. **Manual tests in sandbox environment**  
   Perform manual procedures to verify understanding and operation of the environment.

3. **Final tests**  
   Validate the complete script: signing, authentication, sending, and receiving the approved XML.

---

## Success Criteria

1. The service is able to **sign** and **send** a valid XML invoice, and receive an **approved** response from the tax service, indicating the invoice was accepted.

---

## Suggested Flow

1. Check if the current token has expired (validity: 12 hours).  
2. If expired, request a new one using:  
   - Private key (`.key`)  
   - Valid X.509 certificate (validity: 2 years)  
3. Generate the sales XML.  
4. Sign with OpenSSL(Example command):  
   ```bash
   openssl cms -sign -in MiLoginTicketRequest.xml \
     -out MiLoginTicketRequest.xml.cms \
     -signer certificado_devuelto.pem \
     -inkey MiClavePrivada.key \
     -nodetach -outform PEM
