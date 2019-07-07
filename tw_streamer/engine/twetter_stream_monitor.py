import os
import json
import logging
import random
import redis

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from tw_streamer.utils.redis_utils import check_on_target_word, redis_connect
from tw_streamer.engine.enum_vals import Constants
from tw_streamer.engine.data_processing import process_data


class StreamMonitoringService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def run(self, current_target_word):
        chars = ''.join(random.choices(Constants.ALPHABET, k=10))

        # Credentials
        access_token = os.environ.get('ACCESS_TOKEN', chars)
        access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET', chars)
        consumer_key = os.environ.get("CONSUMER_KEY", chars)
        consumer_secret = os.environ.get("CONSUMER_SECRET", chars)

        #
        if access_token == chars:
            raise EnvironmentError(f"Variable 'ACCESS_TOKEN' is not defined")

        if access_token_secret == chars:
            raise EnvironmentError(f"Variable 'ACCESS_TOKEN_SECRET' is not defined")

        if consumer_key == chars:
            raise EnvironmentError(f"Variable 'CONSUMER_KEY' is not defined")

        if consumer_secret == chars:
            raise EnvironmentError(f"Variable 'CONSUMER_SECRET' is not defined")

        #
        #
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        std_out_listener = StdOutListener(current_target_word)
        stream = Stream(auth, std_out_listener)

        #
        self.logger.info(f"Starting stream service on word '{current_target_word}'")
        stream.filter(track=[current_target_word])


#
class StdOutListener(StreamListener):

    def __init__(self,
                 current_target_word):
        super().__init__()

        # Initialize logger
        self.logger = logging.getLogger(__name__)

        # Set current target name
        self.current_target_word = current_target_word

        # Redis client
        self.redis_client = redis_connect()

        self.logger.info(f"StdOutListener initialized on word '{self.current_target_word}'")

    def on_data(self, data: str) -> bool:
        #
        # Check on target word update
        if not check_on_target_word(self.current_target_word, self.redis_client):
            self.logger.info(f"Current target word was updated. STOP Listening the '{self.current_target_word}' word")
            return False

        data = json.loads(data)

        state = process_data(data)
        self.logger.info(f"Got state: '{state}'")

        if state is None:
            return True

        # 'STATE:STATE_ABBREVIATION'
        key = f'USA:{state}:CITY:{self.current_target_word}'
        self.logger.info(f"KEY: '{key}'")
        try:
            self.redis_client.incr(key, amount=1)
        except (redis.exceptions.AuthenticationError,
                redis.exceptions.ConnectionError):
            self.redis_client = redis_connect()
            self.redis_client.incr(key, amount=1)

        #
        # Here we will extract data from tweet and push it to Redis
        #
        #
        return True

    def on_error(self, status):
        self.logger.error(status)

    # @staticmethod
    # def redis_connect():
    #     n = 0
    #     while n < 120:
    #         try:
    #             return redis.Redis(host=os.environ.get('REDIS_HOST', 'failed_host'), port=6379, db=0)
    #         except redis.exceptions.ConnectionError:
    #             time.sleep(5)
    #             n += 1
    #     # TODO Send notification to user
    #     raise ValueError("PIZDEC POGORELLI !!!")

"""
{
    "created_at": "",
    "id": ,
    "id_str": "",
    "text": "",
    "source": "",
    "truncated": false,
    "in_reply_to_status_id": null,
    "in_reply_to_status_id_str": null,
    "in_reply_to_user_id": null,
    "in_reply_to_user_id_str": null,
    "in_reply_to_screen_name": null,
    "user": {
        "id": ,
        "id_str": "",
        "name": "",
        "screen_name": "",
        "location": "",
        "url": "",
        "description": "",
        "translator_type": "",
        "protected": false,
        "verified": false,
        "followers_count": ,
        "friends_count": ,
        "listed_count": ,
        "favourites_count": ,
        "statuses_count": ,
        "created_at": "",
        "utc_offset": null,
        "time_zone": null,
        "geo_enabled": false,
        "lang": "",
        "contributors_enabled": false,
        "is_translator": false,
        "profile_background_color": "",
        "profile_background_image_url": "",
        "profile_background_image_url_https": "",
        "profile_background_tile": true,
        "profile_link_color": "",
        "profile_sidebar_border_color": "",
        "profile_sidebar_fill_color": "",
        "profile_text_color": "",
        "profile_use_background_image": true,
        "profile_image_url": "",
        "profile_image_url_https":"",
        "profile_banner_url":"",
        "default_profile": false,
        "default_profile_image": false,
        "following": null,
        "follow_request_sent": null,
        "notifications": null
    },
    "geo": null,
    "coordinates": null,
    "place": null,
    "contributors": null,
    "is_quote_status": false,
    "quote_count": 0,
    "reply_count": 0,
    "retweet_count": 0,
    "favorite_count": 0,
    "entities": {
        "hashtags": [],
        "urls": [
            {
                "url": "",
                "expanded_url": "",
                "display_url": "",
                "indices": []
            }
        ],
        "user_mentions": [ 
            {
                "screen_name":"",
                "name":"",
                "id": ,
                "id_str": "",
                "indices": []
            }
        ],
        "symbols":[]
    },
    "favorited": false,
    "retweeted": false,
    "possibly_sensitive": false,
    "filter_level": "low",
    "lang":"", 
    "timestamp_ms":""
}
"""
