import logging


logger = logging.getLogger(__name__)


states = {
    'AL': ('alabama', 'al'),
    'AK': ('alaska', 'ak'),
    'AZ': ('arizona', 'az'),
    'AR': ('arkansas', 'ar'),
    'CA': ('california', 'ca'),
    'CO': ('colorado', 'co'),
    'CT': ('connecticut', 'ct'),
    'DE': ('delaware', 'de'),
    'FL': ('florida', 'fl'),
    'GA': ('georgia', 'ga'),
    'HI': ('hawaii', 'hi'),
    'IL': ('illinois', 'il'),
    'MS': ('mississippi', 'ms'),
    'NJ': ('new jersey', 'nj'),
    'PA': ('pennsylvania', 'pa'),
    'TX': ('texas', "tx"),
    'WI': ('wisconsin', 'wi')
}


def process_data(data: dict):
    try:
        # if data['geo'] is not None or data['coordinates'] is not None:
        #     # logger.info(f"TW: {data}")
        #     pass
        # else:
        #     # logger.info(f"No GEO: {data['user']['location']}")
        #     #
        #     # check on user location
        #     #
        #     pass
        location = data['user']['location']
    except KeyError:
        return None

    #
    #
    if location is None or not isinstance(location, str):
        return None

    #
    #
    location = location.lower()

    words = location.split(',')

    if len(words) == 2:
        # Check on USA in the second place
        if 'usa' in words[1]:
            state = words[0].strip()

            if len(state) == 2:
                return state.upper()
            else:
                for state_abbr, state_words in states.items():
                    if state in state_words:
                        return state_abbr
        else:
            state = words[1].strip()

            for state_abbr, state_words in states.items():
                if state in state_words:
                    return state_abbr
        # logger.debug(f"Got two words: {words}")
    else:
        logger.debug(f"Got more or less than 2 words: {words}")
    return None
