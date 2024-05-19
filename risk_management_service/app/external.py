import logging


logger = logging.getLogger(__file__)

def call_external_api():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('external_api', 5000))
    data = s.recv(1024).decode()
    logger.info(f"External service: {data}")