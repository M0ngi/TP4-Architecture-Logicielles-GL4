FROM python:alpine3.16

RUN  pip install pika

WORKDIR /app

COPY main.py .
COPY app ./app

CMD python3 main.py