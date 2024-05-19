import json
import random
import time
from app.config import Config
from app.helpers import send_msg, create_message
from app.external import call_external_api
import logging

logger = logging.getLogger(__file__)


def new_application_handler(ch, method, properties, body):
    body = json.loads(body)
    
    if body['from'] != Config.COMMERCIAL_SERVICE:
        logger.error(f"Unknown source! Only {Config.COMMERCIAL_SERVICE} can set scores")
        return
    
    app_data = body.get('data', {})
    application = app_data.get('application')
    if application is None:
        logger.error(f"Invalid message, application is null: {body}")
        return
    
    logger.info(f"Reading application: ID={application.get('id')}, score={app_data.get('score')}")

    call_external_api()

    n = random.randint(0, 900000)
    Config.insert_db(n, app_data)

    data = create_message(
        to=Config.OCR_SERVICE,
        data={
            "file_to_text": ['some other files'],
            "nounce": n,
        },
    )
    logger.info(f"Sending to OCR {data}")
    send_msg(
        Config.OCR_INPUT_Q,
        data,
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
    
    app_status = "approved" if random.randint(0, 1) == 1 else "denied"
    data = create_message(
        to=Config.CREDIT_SERVICE,
        data={
            "status": app_status,
            "score": app['score'],
            "application": app['application'],
        },
    )

    logger.info(f"Sending application approval status: {data}")
    send_msg(
        Config.APPROVAL_Q,
        data,
    )
    
    # Sending notification
    data = create_message(
        to=Config.NOTIFICATION_SERVICE,
        data={
            "text": f"Application status: {app_status}",
            "application": app['application'],
        },
    )

    logger.info(f"Sending notification: {data}")
    send_msg(
        Config.NOTIFICATION_Q,
        data,
    )
    
    Config.IN_CHANNEL.basic_ack(delivery_tag)


def run():
    logger.info(f"{Config.APP_NAME} started in 8 seconds...")
    time.sleep(8)
    
    with Config.connect() as _:
        channel = Config.IN_CHANNEL
        
        channel.basic_consume(
            queue=Config.APPLICATION_SCORE_Q,
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
