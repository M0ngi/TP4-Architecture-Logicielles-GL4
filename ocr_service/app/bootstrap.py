import json
import time
import logging

from app.config import Config
from app.storage import read_doc
from app.helpers import create_message, send_msg


logger = logging.getLogger(__file__)


def input_handler(ch, method, properties, body):
    body = json.loads(body)
    
    if (SENDER := body.get('from')) is None:
        logger.error("Unknown sender! Ignoring request")
        return
    
    app_data = body.get('data', {})
    logger.info(f"Reading OCR Request data: {app_data}")
    
    read_doc()

    data = create_message(
        to=SENDER,
        data={
            "text": "OCR Text",
            "nounce": app_data.get("nounce")
        }
    )
    
    send_msg(
        Config.OCR_OUTPUT_Q,
        data,
    )


def run():
    logger.info(f"{Config.APP_NAME} started in 8 seconds...")
    time.sleep(8)
    
    with Config.connect() as _:
        channel = Config.IN_CHANNEL
        
        channel.basic_consume(
            queue=Config.OCR_INPUT_Q,
            on_message_callback=input_handler,
            auto_ack=True,
        )
        
        logger.info("Starting listeners...")
        channel.start_consuming()
