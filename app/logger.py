import logging
from datetime import datetime
import json
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Create a file handler and set its level to DEBUG
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
# Create a stream handler and set its level to INFO
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def log(message, level='INFO'):
    if level == 'DEBUG':
        logger.debug(message)
    elif level == 'INFO':
        logger.info(message)
    elif level == 'WARNING':
        logger.warning(message)
    elif level == 'ERROR':
        logger.error(message)
    elif level == 'CRITICAL':
        logger.critical(message)
    else:
        logger.info(message)
        
