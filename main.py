from classes.splash_uol import SplashUOL
from classes.helpers import Helpers
from classes.twitter import Twitter

import json


def main(request) -> tuple:
    """Function main
    """
    datetime_formatted = Helpers.datetime()

    splash_uol = SplashUOL(poll_path=request.headers['Poll-Endpoint'])
    splash_uol.run()
    poll_data = splash_uol.get_poll_data()

    twitter_session = Twitter(poll_data)
    tweet_data = twitter_session.post(datetime=datetime_formatted)

    poll_data = json.dumps(obj=poll_data, indent=4)

    Helpers.log(
        string_to_log=json.dumps(obj=tweet_data, indent=4),
        file_path='./log/',
        prefix='log_tweet_data'
    )

    Helpers.log(
        string_to_log=json.dumps(obj=poll_data, indent=4),
        file_path='./log/',
        prefix='log_poll'
    )

    return (poll_data, 200)
