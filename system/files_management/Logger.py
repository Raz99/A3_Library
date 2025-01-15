import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename=r'data\logger.txt', encoding='utf-8', level=logging.DEBUG)

def log_success(msg):
    logger.info(msg)

def log_fail(msg):
    logger.error(msg)