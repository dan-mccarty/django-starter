#!/bin/bash
set -e

PROJECT_NAME=DJANGO_STARTER
CERT_DIR="./certs"
DOMAIN=${1:-localhost}

mkdir -p "$CERT_DIR"

echo "Generating self-signed certificate for $DOMAIN..."

openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout "$CERT_DIR/selfsigned.key" \
  -out "$CERT_DIR/selfsigned.crt" \
  -subj "/C=AU/ST=NSW/L=Sydney/O=$PROJECT_NAME/OU=Dev/CN=$DOMAIN"

echo "Certificate and key generated at $CERT_DIR/"
