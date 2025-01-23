import logging
from abc import ABC, abstractmethod

# Set up logging
logging.basicConfig(filename=r'data\logger.txt', encoding='utf-8', level=logging.INFO, format='%(message)s', filemode='a')
logger = logging.getLogger(__name__)

# Component interface
class TextLogger(ABC):
    """
    Abstract base class for text logging components.
    """
    @abstractmethod
    def log(self):
        """
        Logs the text.
        """
        pass

# Concrete component
class SimpleTextLogger(TextLogger):
    """
    A simple text logger that logs plain text.
    """
    def __init__(self, text):
        """
        Initializes the SimpleTextLogger with the given text.

        Args:
            text (str): The text to log.
        """
        self._text = text

    def log(self):
        """
        Returns the text to be logged.

        Returns:
            str: The text to log.
        """
        return self._text

# Decorator abstract class
class TextDecorator(TextLogger, ABC):
    """
    Abstract base class for text logger decorators.
    """
    def __init__(self, text_logger: TextLogger):
        """
        Initializes the TextDecorator with a text logger.

        Args:
            text_logger (TextLogger): The text logger to decorate.
        """
        self._text_logger = text_logger

    @abstractmethod
    def log(self):
        """
        Logs the text with additional behavior.
        """
        pass

# Concrete decorators
class InfoTextDecorator(TextDecorator):
    """
    A text logger decorator that adds info level logging.
    """
    def log(self):
        """
        Logs the text at the info level and returns it.

        Returns:
            str: The text to log.
        """
        try:
            text = self._text_logger.log()  # Get the original text
            logger.info(text)  # Add info logging behavior
            return text  # Maintain the interface contract
        except Exception as e:
            raise RuntimeError("Failed to log info text.") from e

class ErrorTextDecorator(TextDecorator):
    """
    A text logger decorator that adds error level logging.
    """
    def log(self):
        """
        Logs the text at the error level and returns it.

        Returns:
            str: The text to log.
        """
        try:
            text = self._text_logger.log()  # Get the original text
            logger.error(text)  # Add error logging behavior
            return text  # Maintain the interface contract
        except Exception as e:
            raise RuntimeError("Failed to log error text.") from e