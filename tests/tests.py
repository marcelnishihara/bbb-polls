"""Module for tests
"""

from classes.request_analysis import RequestAnalysis
from classes.helpers import Helpers

import json
import requests

from time import sleep
from tqdm import tqdm
from traceback import format_exc


class Test:
    def __init__(self) -> None:
        self.__poll_path = ''


    def get_poll_path(
            self, 
            key: str, 
            index: int, 
            file = './database/polls.json') -> None:
        with open(file=file, mode='r', encoding='utf-8') as polls_file:
            polls = json.loads(s=polls_file.read())
            polls_file.close()
        
        self.__poll_path = polls[key][index]


    def request(self, create_tweet = str, method: str = 'GET') -> str:        
        client_uuid = RequestAnalysis.create_session_uuid_for_tests()

        response = requests.request(
            method=method,
            url='http://0.0.0.0:8080',
            timeout=10,
            headers={
                'Endpoint': self.__poll_path,
                'Tweet': create_tweet,
                'Uuid': client_uuid,
                'Limit': str(3)
            }
        )

        if response.status_code in (200, 201):
            return (
                f'Request Status Code: {response.status_code} | '
                f'Text: {response.text}')

        else:
            return (
                f'Request Status Code: {response.status_code} | '
                f'Error: {response.text}'
            )


if __name__ == '__main__':
    today_is = Helpers.datetime()
    poll_key = 'paredao'
    poll_index = 41
    counter = 0

    while True:
        try:
            create_tweet = False
            tweet_conditions = (
                (counter != 0 and counter % 6 == 0 and counter <= 20) or
                (counter != 0 and counter % 24 == 0 and counter >= 120)
            )

            if tweet_conditions:
                create_tweet = True

            test = Test()
            test.get_poll_path(key=poll_key, index=poll_index)
            test_response = test.request(create_tweet=str(create_tweet))

            msg = (
                f'Request Should Create Tweet: {create_tweet} | '
                f'{test_response} | '
                f'Poll Index: {poll_index} | '
                f'Request Index {counter}')

            print(msg)

            counter += 1

        except Exception:
            Helpers.log(
                today_is=today_is['formatted'],
                string_to_log=json.dumps(
                    obj={
                        'error': format_exc().replace("\n", " ")
                    }, 
                    indent= 4
                ),
                file_path='./log/',
                prefix='log_tests_error'
            )

            print('\nSomenthing went wrong with Tests script. Error Logged.\n')

        time_to_next_process = 300

        for _ in tqdm(range(time_to_next_process), desc="Next Request: "):
            sleep(1)
