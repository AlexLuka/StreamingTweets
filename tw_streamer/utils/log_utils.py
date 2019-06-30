import sys
import logging

from logging.handlers import TimedRotatingFileHandler


def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s")

    # Add handler 1
    handler1 = logging.StreamHandler(sys.stdout)
    handler1.setFormatter(formatter)
    logger.addHandler(handler1)

    # Add handler 2
    handler2 = TimedRotatingFileHandler(
        "/home/alelu/Coding/TweeterAPI/logs//logfile",
        when='h',
        interval=1,
        backupCount=10
    )
    handler2.setFormatter(formatter)
    logger.addHandler(handler2)
    return logger
