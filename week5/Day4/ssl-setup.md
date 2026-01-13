SSL Setup Using mkcert and NGINX
Objective

Enable HTTPS locally using a trusted certificate and terminate TLS at NGINX while keeping backend services on HTTP.

Local Domain

A local domain is used to simulate a production environment.

127.0.0.1 myapp.local

Certificate Generation

A local Certificate Authority is installed using mkcert.

mkcert -install


A certificate and private key are generated for the local domain.

mkcert myapp.local

HTTPS Flow

HTTP requests are redirected to HTTPS.
NGINX presents the SSL certificate and completes the TLS handshake.
Encrypted traffic is decrypted at NGINX and forwarded to the backend over HTTP.
Responses are encrypted again before being sent to the client.

Verification

The application is accessed using the local domain over HTTPS.
A lock icon in the browser confirms a valid and trusted secure connection.

Summary

HTTPS is enabled using mkcert and NGINX.
TLS is terminated at NGINX.
Backend services communicate over HTTP within the Docker network.