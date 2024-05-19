FROM python:alpine3.16

RUN apk update
RUN apk add socat

WORKDIR /app

COPY main.py .
COPY app ./app
COPY entrypoint.sh .

RUN chmod +x /app/entrypoint.sh
CMD /app/entrypoint.sh