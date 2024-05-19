import logging
import sys
from app.bootstrap import run

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stderr)])

__all__ = [
    'run',
]