import re
from logging import getLogger, Logger
from typing import Any

from django.core.exceptions import ValidationError


class BaseService:
    """
    A base service class providing logging functionality for derived classes.
    Each service instantiated from this class will have a logger specific to its class name.
    """

    def __init__(self):
        """
        Initializes the BaseService instance and sets up a logger specific to the class.
        """
        self.logger: Logger = self._initialize_logger()

    def _initialize_logger(self) -> Logger:
        """
        Creates and returns a logger instance specific to the current class name.

        Returns:
            Logger: A logger instance for the class.
        """
        return getLogger(self.__class__.__name__)

    def log(self, level: int, message: str, *args: Any, **kwargs: Any) -> None:
        """
        Logs a message at the specified logging level.

        Args:
            level (int): The logging level (e.g., logging.INFO, logging.ERROR).
            message (str): The message to log.
            *args (Any): Optional positional arguments for string formatting in the log message.
            **kwargs (Any): Optional keyword arguments for the logger.
        """
        self.logger.log(level=level, msg=message, *args, **kwargs)

    @staticmethod
    def regex_validator(value: Any, pattern: str, error_message: str) -> str:
        """
        Validates a string value against a provided regular expression.

        Args:
            value (Any): The value to be validated.
            pattern (str): The regular expression pattern for validation.
            error_message (str): The error message to raise in case of invalid input.

        Returns:
            str: The validated value if it matches the pattern.

        Raises:
            ValidationError: If the value does not match the given pattern.
        """
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")

        if re.fullmatch(pattern, value):
            return value
        else:
            raise ValidationError(error_message)
