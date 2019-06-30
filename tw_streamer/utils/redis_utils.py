import logging


logger = logging.getLogger(__name__)


def check_on_target_word(current_target_word: str) -> bool:
    logger.info(f"Check on target word update")
    # Get new target word
    new_target_word = get_target_word()
    logger.debug(f"Got new target word '{new_target_word}', current_target_word = '{current_target_word}'")

    if current_target_word != new_target_word:
        logger.info(f"New target word is different. Update required!")
        return False
    logger.info(f"Target word is the same. No update")
    return True


def get_target_word() -> str:
    return 'the'
