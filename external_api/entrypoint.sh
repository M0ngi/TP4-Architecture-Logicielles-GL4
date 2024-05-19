#!/bin/sh

echo "External Service API Started"

socat TCP-LISTEN:5000,reuseaddr,fork EXEC:"python3 /app/main.py",pty,stderr
