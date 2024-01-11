from classes.helpers import Helpers
from classes.request_analysis import RequestAnalysis
from classes.splash_uol import SplashUOL
from classes.twitter import Twitter

import json


def main(request) -> tuple:
    """Function main
    """
    today_is = Helpers.datetime()

    is_valid_request, explanation = RequestAnalysis.is_valid_request(
        headers=request.headers
    )

    if is_valid_request:
        splash_uol = SplashUOL(
            today_is=today_is['formatted'],
            poll_path=request.headers['Endpoint'])
        splash_uol.run()
        poll_data = splash_uol.get_poll_data()

        Helpers.log(
            today_is=today_is['formatted'],
            string_to_log=json.dumps(obj=poll_data, indent=4),
            file_path='./log/',
            prefix='log_poll'
        )

        create_tweet = RequestAnalysis.create_tweet(
            bool_as_string=request.headers['Tweet']
        )

        if create_tweet:
            twitter_session = Twitter(poll_data)
            tweet_data = twitter_session.post(today_is=today_is)

            Helpers.log(
                today_is=today_is['formatted'],
                string_to_log=json.dumps(obj=tweet_data, indent=4),
                file_path='./log/',
                prefix='log_tweet_data'
            )

        return ('OK', 200)

    else:
        bad_request_json = json.dumps(
            obj={
                'badRequest': True, 
                'todayIs': today_is['formatted'],
                'explanation': explanation
            },
            indent=4
        )

        Helpers.log(
            today_is=today_is['formatted'],
            string_to_log=bad_request_json,
            file_path='./log/',
            prefix='log_bad_request'
        )

        return ('Bad Request', 400)
