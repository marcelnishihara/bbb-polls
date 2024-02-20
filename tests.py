"""Module for tests
"""

from classes.request_analysis import RequestAnalysis
from classes.bets import Bets

import json
import requests

from time import sleep


class Test:
    def __init__(self) -> None:
        self.__poll_path = ''


    def get_poll_path(
            self, 
            key: str, 
            index: int, 
            file = './polls.json') -> None:
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
                'Uuid': client_uuid
            }
        )

        return (
            f'Request Status Code: {response.status_code} | '
            f'Text: {response.text}')


    @staticmethod
    def bets() -> dict:
        bets = Bets()
        bets.run()


if __name__ == '__main__':
    counter = 0

    while True:
        create_tweet = False

        if counter % 30 == 0:
            create_tweet = True

        test = Test()
        test.get_poll_path(key='paredao', index=8)
        test_response = test.request(create_tweet=str(create_tweet))

        msg = (
            f'Create Tweet: {create_tweet} | '
            f'{test_response} | '
            f'Request Index {counter}')

        print(msg)
        sleep(120)
        counter += 1
