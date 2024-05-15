
"""
Logger Definition.

"""
import os
import logging
import datetime
from pythonjsonlogger import jsonlogger


class Logger(logging.Logger):
    """
    Defining Logger to log to log_path.
    """

    _logger = None

    def __new__(cls, *args, **kwargs):
        if cls._logger is None:

            cls._logger = super().__new__(cls, *args, **kwargs)
            cls._logger = logging.getLogger("main_logger")
            log_level = os.environ.get("LOG_LEVEL", "info")
            log_level = log_level.lower()

            if log_level == "info":
                cls._logger.setLevel(logging.INFO)
            elif log_level == "debug":
                cls._logger.setLevel(logging.DEBUG)
            elif log_level == "warning":
                cls._logger.setLevel(logging.WARNING)
            elif log_level == "error":
                cls._logger.setLevel(logging.ERROR)

            # formatter = logging.Formatter(
            #     '%(asctime)s \t [%(levelname)s | %(filename)s:%(funcName)s:%(lineno)s] > %(message)s')

            now = datetime.datetime.now()
            cls.dirname = "."

            if not os.path.isdir(cls.dirname):
                os.mkdir(cls.dirname)

            fileHandler = logging.FileHandler(
                cls.dirname + "/log_" + now.strftime("%Y-%m-%d") + ".log")

            streamHandler = logging.StreamHandler()

            # fileHandler.setFormatter(formatter)
            # streamHandler.setFormatter(formatter)

            # Will log out in json format so that output is machine-readable
            fileHandler.setFormatter(jsonlogger.JsonFormatter(
                '%(name)s %(asctime)s [%(levelname)s] %(filename)s:%(lineno)d %(message)s'
            ))

            # Will log out in json format so that output is machine-readable
            streamHandler.setFormatter(jsonlogger.JsonFormatter(
                '%(name)s %(asctime)s [%(levelname)s] %(filename)s:%(lineno)d %(message)s'
            ))

            # cls._logger.addHandler(fileHandler)
            cls._logger.addHandler(streamHandler)

        return cls._logger

    @classmethod
    def set_log_level(cls, level):
        """
        Set the log level of the logger.
        """
        cls._logger.setLevel(level)

    @classmethod
    def get_log_level(cls):
        """
        Get the log level of the logger.
        """
        return cls._logger.getEffectiveLevel()


logger = Logger()
