import os
from time import sleep

from tw_streamer.utils.log_utils import init_logger
from tw_streamer.engine.twetter_stream_monitor import StreamMonitoringService
from tw_streamer.utils.redis_utils import get_target_word, redis_connect


# Variables that contains the user credentials to access Twitter API
# access_token = os.environ.get('ACCESS_TOKEN')
# access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
# consumer_key = os.environ.get("CONSUMER_KEY")
# consumer_secret = os.environ.get("CONSUMER_SECRET")


# In Redis:
#   Key: STATE in format USA:TX, USA:IL, etc...


def main():
    # target_word = 'the'

    while True:
        # Monitor some specific word in twitter
        #
        # 1. Check on word update
        logger.info(f"Checking whether the target word require an update")
        target_word = get_target_word(redis_client=redis_connect())

        # 2. Run word monitoring service
        logger.info(f"Start monitoring service for word '{target_word}''")
        StreamMonitoringService().run(target_word)

        sleep(5)


if __name__ == '__main__':
    logger = init_logger()

    # os.environ['REDIS_HOST'] = 'localhost'
    logger.info(f"REDIS_HOST = {os.environ.get('REDIS_HOST')}")

    main()
