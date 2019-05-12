import os
import sys
import json
import logging

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


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


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data: str):
        data = json.loads(data)
        if data['geo'] is not None or data['coordinates'] is not None:
            logger.info(f"TW: {data}")
        else:
            logger.info(f"No GEO: {data['user']['location']}")
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
    stream.filter(track=['tesla', 'Elon Musk', 'ElonMusk'])


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Add handler
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    main()
