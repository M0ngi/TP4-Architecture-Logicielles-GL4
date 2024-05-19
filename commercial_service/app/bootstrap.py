import json
import random
import time
from app.helpers import send_msg, create_message
from app.config import Config
import logging

logger = logging.getLogger(__file__)


def new_application_handler(ch, method, properties, body):
    body = json.loads(body)
    
    if body['from'] != Config.APPLICATION_SERVICE:
        logger.error(f"Unknown source! Only {Config.APPLICATION_SERVICE} can create new applications")
        return
    
    app_data = body.get('data', {})
    logger.info(f"Reading new application: ID={app_data.get('id')}")

    n = random.randint(0, 900000)
    data = create_message(
        to=Config.OCR_SERVICE,
        data={
            "file_to_text": app_data.get('files', []),
            "nounce": n,
        }
    )
    Config.insert_db(n, app_data)

    logger.info(f"Sending to OCR {data}")
    send_msg(
        Config.OCR_INPUT_Q,
        data
    )


def ocr_result_handler(ch, method, properties, body):
    delivery_tag = method.delivery_tag
    body = json.loads(body)
    
    if body.get('to') != Config.APP_NAME:
        Config.IN_CHANNEL.basic_nack(delivery_tag)
        return

    data = body.get('data', {'text': ''})
    app_nounce = data.get('nounce')
    if not Config.row_exist_db(app_nounce):
        logger.error(f"Unknown application reference {app_nounce}")
        logger.error(f"DB {Config.DB}")
        Config.IN_CHANNEL.basic_ack(delivery_tag)
        return
    
    app = Config.read_db(app_nounce)
    
    logger.info(f"Reading result OCR {data}")
    logger.info(f"Application reference: {app}")
    
    data = create_message(
        to=Config.RISK_MANAGEMENT_SERVICE,
        data={
            "score": random.randint(0, 20),
            "application": app,
        }
    )

    logger.info(f"Sending application score: {data}")
    send_msg(
        Config.APPLICATION_SCORE_Q,
        data
    )
    
    Config.IN_CHANNEL.basic_ack(delivery_tag)


def run():
    logger.info(f"{Config.APP_NAME} started in 8 seconds...")
    time.sleep(8)
    
    with Config.connect() as _:
        channel = Config.IN_CHANNEL
        
        channel.basic_consume(
            queue=Config.APPLICATION_Q,
            on_message_callback=new_application_handler,
            auto_ack=True,
        )
        
        channel.basic_consume(
            queue=Config.OCR_OUTPUT_Q,
            on_message_callback=ocr_result_handler,
            auto_ack=False,
        )
        
        logger.info("Starting listeners...")
        channel.start_consuming()
