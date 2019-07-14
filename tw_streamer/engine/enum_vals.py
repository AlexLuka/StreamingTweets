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

    STATES = {
        'AL': ('alabama', 'al'),
        # 'AK': ('alaska', 'ak'),
        'AZ': ('arizona', 'az'),
        'AR': ('arkansas', 'ar'),
        'CA': ('california', 'ca'),
        'CO': ('colorado', 'co'),
        'CT': ('connecticut', 'ct'),
        'DE': ('delaware', 'de'),
        'FL': ('florida', 'fl'),
        'GA': ('georgia', 'ga'),
        # 'HI': ('hawaii', 'hi'),
        'IL': ('illinois', 'il'),
        'MS': ('mississippi', 'ms'),
        'NJ': ('new jersey', 'nj'),
        'PA': ('pennsylvania', 'pa'),
        'TX': ('texas', "tx"),
        'WI': ('wisconsin', 'wi')
    }
