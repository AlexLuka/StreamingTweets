import logging


logger = logging.getLogger(__name__)


states = {
    'alabama': 'al',
    'alaska': 'ak',
    'illinois': 'il',
    'mississippi': 'ms',
    'texas': "tx",
    'wisconsin': 'wi'
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
                return state
            else:
                try:
                    return states[state]
                except KeyError:
                    return None
        else:
            state = words[1].strip()

            try:
                return states[state]
            except KeyError:
                if state in states.values():
                    return state
                return None



        # logger.debug(f"Got two words: {words}")
    else:
        logger.debug(f"Got more or less than 2 words: {words}")
