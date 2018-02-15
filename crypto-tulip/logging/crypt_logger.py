"""

Logger Modular
"""

import logging
from enum import Enum
import json
import inspect


class LoggingLevel(Enum):
    """
    Enumerator to specify the logging level
    """
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0



class Logger:
    """
    The Logger Class that has static methods to help with different logging
    """


    @staticmethod
    def generate_logger(level, filename, output_format, loggername):
        """ Generates and returns the logger object

        Keyword arugments:
        level -- Type of Logging Level
        filename -- The file that the logged messages will be saved to
        output_format -- The format the data will be logged in
        loggername -- the logger id name

        Returns:
        logger -- the logger object so the log function can log appropriately
        """
        handler = logging.FileHandler(filename)
        handler.setFormatter(logging.Formatter(output_format))
        logger = logging.getLogger(loggername)
        logger.setLevel(level)
        logger.addHandler(handler)
        return logger

    @staticmethod
    def setup_logger(level):
        """ Parses the json settings to be sent to the logger generater

        Keyword arugments:
        level -- the type of logging they want base on the ENUM Logging Level

        Returns:
        logger -- the logger object so the log function can log appropriately
        """
        data = json.load(open('logging.json'))
        if level == LoggingLevel.DEBUG:
            logger = Logger.generate_logger(
                level.value,
                data["handlers"]["debug_file_handler"]["filename"],
                data["formatters"]["defaultWithStack"]["format"],
                data["handlers"]["debug_file_handler"]["name"]
                )
        elif level == LoggingLevel.INFO:
            logger = Logger.generate_logger(
                level.value,
                data["handlers"]["info_file_handler"]["filename"],
                data["formatters"]["default"]["format"],
                data["handlers"]["info_file_handler"]["name"]
                )
        elif level == LoggingLevel.ERROR:
            logger = Logger.generate_logger(
                level.value,
                data["handlers"]["error_file_handler"]["filename"],
                data["formatters"]["defaultWithStack"]["format"],
                data["handlers"]["error_file_handler"]["name"]
                )
        elif level == LoggingLevel.CRITICAL:
            logger = Logger.generate_logger(
                level.value,
                data["handlers"]["critical_file_handler"]["filename"],
                data["formatters"]["defaultWithStack"]["format"],
                data["handlers"]["critical_file_handler"]["name"]
                )
        return logger

    @staticmethod
    def log(message, issue_level, logging_level, stack_trace=''):
        """ The static method that the user will call to log to a specific file given the parameters
        Keyword arugments:
        message -- message the send to be logged
        issue_level -- Custom user error code
        logging_level -- How they want the message to be logged
        stack -- the stack trace to be loged

        Returns:
        """
        logger = Logger.setup_logger(logging_level)
        function_call = inspect.stack()
        if logging_level == LoggingLevel.DEBUG:
            logger.debug('debug message %s: ', message + " The Issue Level is: " + str(issue_level), extra={'functioncall': str(function_call[1][4]), 'Stacktrace': stack_trace})
        elif logging_level == LoggingLevel.INFO:
            logger.info(message)
        elif logging_level == LoggingLevel.ERROR:
            logger.error('Error Message %s: ', message + " The Issue Level is: " + str(issue_level), extra={'functioncall': str(function_call[1][4]), 'Stacktrace': stack_trace})
        elif logging_level == LoggingLevel.CRITICAL:
            logger.critical('Critical message %s: ', message + " The Issue Level is: " + str(issue_level), extra={'functioncall': str(function_call[1][4]), 'Stacktrace': stack_trace})
