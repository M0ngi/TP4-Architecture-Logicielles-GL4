import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika import BlockingConnection

class Config:
    HOST = "rabbitmq"
    RMQ_CONNECTION = pika.ConnectionParameters(HOST, heartbeat=0)
    
    APPLICATION_Q = "application_q"
    APPLICATION_SCORE_Q = "application_score_q"
    APPROVAL_Q = "approval_q"
    OCR_INPUT_Q = "ocr_input_q"
    OCR_OUTPUT_Q = "ocr_output_q"
    NOTIFICATION_Q = "notifications_q"
    
    ALL_Q = [
        APPLICATION_Q,
        APPLICATION_SCORE_Q,
        APPROVAL_Q,
        OCR_INPUT_Q,
        OCR_OUTPUT_Q,
        NOTIFICATION_Q,
    ]
    
    APPLICATION_SERVICE = "application_service"
    COMMERCIAL_SERVICE = "commercial_service"
    NOTIFICATION_SERVICE = "notification_service"
    OCR_SERVICE = "ocr_service"
    RISK_MANAGEMENT_SERVICE = "risk_management_service"
    CREDIT_SERVICE = "credit_service"
    
    APP_NAME = NOTIFICATION_SERVICE
    
    CONNECTION: BlockingConnection = None
    IN_CHANNEL: BlockingChannel = None
    OUT_CHANNEL: BlockingChannel = None
    
    @staticmethod
    def connect():
        if Config.CONNECTION is None:
            Config.CONNECTION = connection = pika.BlockingConnection(Config.RMQ_CONNECTION)
            Config.IN_CHANNEL = connection.channel()
            Config.OUT_CHANNEL = connection.channel()
            
            for q in Config.ALL_Q:
                Config.OUT_CHANNEL.queue_declare(q, durable=True)
        
        return connection
