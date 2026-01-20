from classes.helpers import Helpers
from classes.request_analysis import RequestAnalysis
from classes.splash_uol import SplashUOL
from classes.twitter import Twitter

import flask
import json

from traceback import format_exc


def process(request: flask.Request, today_is: dict) -> tuple:
    """Function process
    """
    splash_uol = SplashUOL(
            today_is=today_is['formatted'],
            poll_path=request.headers['Endpoint']
    )

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

    tuple_to_return = ('Poll Data Logged', 200)

    if create_tweet:
        if RequestAnalysis.is_valid_limit(headers=request.headers):
            counter_limit = int(request.headers['Limit'])
        else:
            counter_limit = 3

        twitter_session = Twitter(poll_data)
        tweet_data = twitter_session.post(
            today_is=today_is, 
            counter_limit=counter_limit
        )

        Helpers.log(
            today_is=today_is['formatted'],
            string_to_log=json.dumps(obj=tweet_data, indent=4),
            file_path='./log/',
            prefix='log_tweet_data'
        )

        if tweet_data['success']:
            tuple_to_return = ('Tweet Created', 201)
        else:
            tuple_to_return = ('Tweet Too Long', 413)

    return tuple_to_return


def main(request) -> tuple:
    """Function main
    """
    today_is = Helpers.datetime()

    is_valid_request, explanation = RequestAnalysis.is_valid_request(
        headers=request.headers
    )

    try:
        if is_valid_request:
            tuple_to_return = process(request=request, today_is=today_is)
            return tuple_to_return

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

            return (bad_request_json, 400)

    except Exception:
        return (format_exc().replace('\n', ' '), 500)
