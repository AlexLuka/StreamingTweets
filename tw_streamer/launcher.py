# import os
# import sys
import json
# import logging

# ?\from logging.handlers import TimedRotatingFileHandler
from time import sleep

# import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from tw_streamer.utils.log_utils import init_logger
from tw_streamer.engine.twetter_stream_monitor import StreamMonitoringService


# Variables that contains the user credentials to access Twitter API
# access_token = os.environ.get('ACCESS_TOKEN')
# access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
# consumer_key = os.environ.get("CONSUMER_KEY")
# consumer_secret = os.environ.get("CONSUMER_SECRET")


# In Redis:
#   Key: STATE in format USA:TX, USA:IL, etc...


def main():
    the_word = 'the'

    while True:
        # Monitor some specific word in twitter
        #
        # 1. Check on word update
        logger.info(f"Checking whether the target word require an update")

        # 2. Run word monitoring service
        logger.info(f"Start monitoring service for word '{the_word}''")
        StreamMonitoringService().run(the_word)

        sleep(5)


if __name__ == '__main__':
    logger = init_logger()

    main()
