import os
import logging
import redis
import time
import traceback

from tw_streamer.engine .enum_vals import Constants


logger = logging.getLogger(__name__)


def check_on_target_word(
        current_target_word: str,
        redis_client: redis.Redis) -> bool:
    logger.debug(f"Check on target word update")
    # Get new target word
    new_target_word = get_target_word(redis_client)
    logger.debug(f"Got new target word '{new_target_word}', current_target_word = '{current_target_word}'")

    if current_target_word != new_target_word:
        logger.debug(f"New target word is different. Update required!")
        return False
    logger.debug(f"Target word is the same. No update")
    return True


def redis_connect():
    n = 0
    while n < 120:
        try:
            return redis.Redis(host=os.environ.get('REDIS_HOST', 'failed_host'), port=6379, db=0)
        except redis.exceptions.ConnectionError:
            time.sleep(5)
            n += 1
    # TODO Send notification to user
    raise ValueError("PIZDEC POGORELLI !!!")


def get_target_word(redis_client: redis.Redis) -> str:
    # rc = redis.Redis(host=os.environ.get('REDIS_HOST'), port=6379, db=0)

    while True:
        try:
            target_word = redis_client.get(Constants.TARGET_WORD_KEY).decode('utf-8')

            if target_word is None:
                logger.warning(f"Failed to find a target word, going to use "
                               f"the default one: {Constants.DEFAULT_TARGET_WORD}")
                target_word = Constants.DEFAULT_TARGET_WORD

            break
        except Constants.REDIS_EXCEPTIONS:
            logger.warning(f"Failed to get target word because of exception")
            logger.exception(traceback.format_exc())
            time.sleep(5)

    return target_word
