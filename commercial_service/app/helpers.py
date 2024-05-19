import json
from app.config import Config


def send_msg(queue, data: dict):
    data_str = json.dumps(data)
    channel = Config.OUT_CHANNEL
    
    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=data_str,
    )


def create_message(to, data):
    return {
        "from": Config.APP_NAME,
        "to": to,
        "data": data,
    }
