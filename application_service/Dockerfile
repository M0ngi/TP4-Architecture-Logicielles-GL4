FROM python:alpine3.16

RUN apk update
RUN apk add socat

RUN pip install pika

WORKDIR /app

COPY main.py .
COPY app ./app

# CMD python3 main.py
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"python3 /app/main.py",pty,stderr