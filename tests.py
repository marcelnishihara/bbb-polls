"""Module for tests
"""

from classes.request_analysis import RequestAnalysis

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


    def request(self, create_tweet = str) -> str:        
        client_uuid = RequestAnalysis.create_session_uuid_for_tests()

        response = requests.request(
            method='GET',
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


if __name__ == '__main__':
    counter = 1

    while True:
        create_tweet = False

        if counter % 120 == 0:
            create_tweet = True
        
        test = Test()
        test.get_poll_path(key='paredao', index=6)
        test_response = test.request(create_tweet=str(create_tweet))

        print(test_response)
        sleep(120)
        counter += 1
