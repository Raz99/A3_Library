import logging
from abc import ABC, abstractmethod

# Set up logging
logging.basicConfig(filename=r'data\logger.txt', encoding='utf-8', level=logging.INFO, format='%(message)s', filemode='a')
logger = logging.getLogger(__name__)


# Component interface
class TextLogger(ABC):
    @abstractmethod
    def log(self):
        pass


# Concrete component
class SimpleTextLogger(TextLogger):
    def __init__(self, text):
        self._text = text

    def log(self):
        return self._text


# Decorator abstract class
class TextDecorator(TextLogger, ABC):
    def __init__(self, text_logger: TextLogger):
        self._text_logger = text_logger

    @abstractmethod
    def log(self):
       pass


# Concrete decorators
class InfoTextDecorator(TextDecorator):
    def log(self):
        try:
            text = self._text_logger.log()  # Get the original text
            logger.info(text)  # Add info logging behavior
            return text  # Maintain the interface contract
        except Exception as e:
            raise RuntimeError("Failed to log info text.") from e

class ErrorTextDecorator(TextDecorator):
    def log(self):
        try:
            text = self._text_logger.log()  # Get the original text
            logger.error(text)  # Add error logging behavior
            return text  # Maintain the interface contract
        except Exception as e:
            raise RuntimeError("Failed to log error text.") from e