FROM nginx:alpine
LABEL maintainer="Wazo <dev@wazo.io>"
ENV VERSION 0.1.0

RUN apk add openssl && \
    openssl req -x509 -nodes -days 365 \
    -subj "/C=CA/ST=QC/O=Company, Inc./CN=mydomain.com" \
    -addext "subjectAltName=DNS:mydomain.com" \
    -newkey rsa:2048 \
    -keyout /etc/ssl/private/nginx-selfsigned.key \
    -out /etc/ssl/certs/nginx-selfsigned.crt;

COPY ./default.conf /etc/nginx/conf.d/default.conf
