import json
import time
from app.config import Config
import logging

logger = logging.getLogger(__file__)

def notification_handler(ch, method, properties, body):
    body = json.loads(body)

    logger.info(f"New notification: {body}")


def run():
    logger.info(f"{Config.APP_NAME} started in 8 seconds...")
    time.sleep(8)
    
    with Config.connect() as _:
        channel = Config.IN_CHANNEL
        
        channel.basic_consume(
            queue=Config.NOTIFICATION_Q,
            on_message_callback=notification_handler,
            auto_ack=True,
        )
        
        logger.info("Starting listeners...")
        channel.start_consuming()
