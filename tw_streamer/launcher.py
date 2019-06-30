import os
import sys
import json
import logging

from logging.handlers import TimedRotatingFileHandler

import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from tw_streamer.utils.log_utils import init_logger


# Variables that contains the user credentials to access Twitter API
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")


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


# In Redis:
#   Key: STATE in format USA:TX, USA:IL, etc...


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data: str) -> bool:
        data = json.loads(data)
        try:
            if data['geo'] is not None or data['coordinates'] is not None:
                #
                # This is valid only if GPS coordinates are present
                #   Check whether coordinates are inside the state polygon
                #
                #
                logger.info(f"TW: {data}")
                pass
            else:
                #
                # Get the location: str
                location = data['user']['location']

                if location is None:
                    return True

                # Parse the location string to get STATE
                # Check only tweets with location in format:
                #   CITY, STATE
                #   STATE, COUNTRY, where country == USA

                # Convert string to lower string
                location = location.lower()

                #
                #
                #
                logger.info(f"No GEO: {data['user']['location']}")
                # pass
            return True
        except KeyError:
            return True

    def on_error(self, status):
        logger.error(status)


def main():
    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    # stream.filter(track=['l'])
    stream.filter(track=['the'])


if __name__ == '__main__':
    logger = init_logger()

    main()
