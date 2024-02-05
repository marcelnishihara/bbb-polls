"""Module for tests
"""

from classes.request_analysis import RequestAnalysis

import json
import requests

from time import sleep


if __name__ == '__main__':
    with open(file='./polls.json', mode='r', encoding='utf-8') as polls_file:
        polls = json.loads(s=polls_file.read())
        polls_file.close()

    counter = 0
    current_poll = polls['paredao'][6]

    while True:
        create_tweet = False

        if counter % 60 == 0:
            create_tweet = True

        print(f'Counter: {counter}. Create Tweet: {create_tweet}')

        client_uuid = RequestAnalysis.create_session_uuid_for_tests()

        response = requests.request(
            method='GET',
            url='http://0.0.0.0:8080',
            timeout=10,
            headers={
                'Endpoint': current_poll,
                'Tweet': str(create_tweet),
                'Uuid': client_uuid
            }
        )

        response_msg = (
            f'Request Status Code: {response.status_code} | '
            f'Text: {response.text}')

        print(response_msg)
        sleep(120)
        counter += 1
