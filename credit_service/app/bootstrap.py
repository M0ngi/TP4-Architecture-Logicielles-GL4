import json
import time
from app.config import Config
from app.helpers import send_msg, create_message
from app.storage import write_doc
import logging

logger = logging.getLogger(__file__)


def approval_handler(ch, method, properties, body):
    body = json.loads(body)
    
    if body['from'] != Config.RISK_MANAGEMENT_SERVICE:
        logger.error(f"Unknown source! Only {Config.RISK_MANAGEMENT_SERVICE} can set scores")
        return
    
    app_data = body.get('data', {})
    application = app_data.get('application')
    if application is None:
        logger.error(f"Invalid message, application is null: {body}")
        return
    
    logger.info(f"Reading application: ID={application.get('id')}, status={app_data.get('status')}")

    write_doc()

    # Sending notification
    data = create_message(
        to=Config.NOTIFICATION_SERVICE,
        data={
            "text": "Your document is ready at: [doc link]",
            "application": application,
        },
    )

    logger.info(f"Sending notification: {data}")
    send_msg(
        Config.NOTIFICATION_Q,
        data,
    )


def run():
    logger.info(f"{Config.APP_NAME} started in 8 seconds...")
    time.sleep(8)
    
    with Config.connect() as _:
        channel = Config.IN_CHANNEL
        
        channel.basic_consume(
            queue=Config.APPROVAL_Q,
            on_message_callback=approval_handler,
            auto_ack=True,
        )
        
        logger.info("Starting listeners...")
        channel.start_consuming()
