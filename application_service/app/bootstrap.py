import json
import random
import time
from app.config import Config
import logging

logger = logging.getLogger(__file__)


def run():
    logger.info(f"{Config.APP_NAME} started.")
    
    with Config.connect() as _:
        channel = Config.OUT_CHANNEL
        
        while True:
            logger.info("Sending new application")
            
            application_email = input("Contact Email: ")
            file_url = input("File: ")
            
            data = {
                "from": Config.APP_NAME,
                "to": Config.COMMERCIAL_SERVICE,
                "data": {
                    "id": random.randint(0, 500),
                    "files": [file_url],
                    "email": application_email,
                    "meta": "new application"
                },
            }
            
            body = json.dumps(data)
            channel.basic_publish(exchange="", routing_key=Config.APPLICATION_Q, body=body)
            
            time.sleep(5)
