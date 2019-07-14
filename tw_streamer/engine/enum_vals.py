import redis.exceptions as ex


class Constants:
    ALPHABET = "abcdefghijklmnopqrstuvwxyz1234567890"

    TARGET_WORD_KEY = "TARGET_WORD"
    DEFAULT_TARGET_WORD = "the"

    REDIS_EXCEPTIONS = (
        ex.ConnectionError,
        ex.AuthenticationError,
        ex.BusyLoadingError,
        ex.DataError,
        ex.LockError,
        ex.InvalidResponse,
        ex.TimeoutError,
        ex.NoScriptError
    )
