"""Module for Security
"""

from classes.helpers import Helpers

import os
import requests
import uuid

from typing import Dict, List, Union, Tuple


class RequestAnalysis:
    @staticmethod
    def __create_uuid_name_parameter() -> str:
        """Private Static Method __create_uuid_name_parameter
        """
        helpers_datetime = Helpers.datetime()
        
        uuid_name = [
            int(helpers_datetime["now"].year),
            int(helpers_datetime["now"].month),
            int(helpers_datetime["now"].day),
            int(helpers_datetime["now"].hour),
            int(helpers_datetime["now"].minute)
        ]

        for index, value in enumerate(uuid_name):
            if value < 10:
                uuid_name[index] = f'0{value}'
            else:
                uuid_name[index] = str(value)
        
        return '_'.join(uuid_name)


    @staticmethod
    def __create_session_uuid(uuid_name: str) -> str:
        """Private Static Method __generate_session_uuid
        """
        namespace = uuid.UUID(hex=os.environ['UUID'])
        return str(uuid.uuid5(namespace=namespace, name=uuid_name))


    @staticmethod
    def __is_valid_endpoint(endpoint: str) -> bool:
        """Private Static Method __is_valid_endpoint
        """
        poll_url_prefix = 'https://www.uol.com.br/splash/bbb/enquetes'
        
        if endpoint.startswith('/'):
            url = f'{poll_url_prefix}{endpoint}'
            response = requests.request(method='GET', url=url, timeout=2)
            return True if response.status_code == 200 else False
        else:
            return False


    @staticmethod
    def create_session_uuid_for_tests() -> str:
        uuid_name = RequestAnalysis.__create_uuid_name_parameter()
        return RequestAnalysis.__create_session_uuid(uuid_name=uuid_name)


    @staticmethod
    def is_valid_request(
        headers: Dict[str, str]
        ) -> Tuple[bool, Union[None, List]]:
        """Public Static Method is_valid_request
        """
        uuid_name = RequestAnalysis.__create_uuid_name_parameter()
        session_uuid = RequestAnalysis.__create_session_uuid(
            uuid_name=uuid_name
        )

        is_valid_uuid = session_uuid == headers['Uuid']
        is_valid_tweet = headers['Tweet'].lower() in ('true', 'false')

        is_valid_endpoint = RequestAnalysis.__is_valid_endpoint(
            endpoint=headers['Endpoint']
        )

        request_not_valid = [
            {
                'isValidUUID': is_valid_uuid,
                'error': (
                    'If "isValidUUID" is False, '
                    'the UUID is incorrect')
            },
            {
                'isValidTweet': is_valid_tweet,
                'error': (
                    'This parameter tells the script if a tweet will be '
                    'created and posted. The value expected for this is '
                    'a boolean parsed into string')
            },
            {
                'isValidEndpoint': is_valid_endpoint,
                'error': (
                    'Missing the dash character or the page status code '
                    'is different from 200'
                )
            }
        ]

        is_valid_request = (
            is_valid_uuid and 
            is_valid_tweet and
            is_valid_endpoint)

        return (True, None) if is_valid_request else (False, request_not_valid) 


    @staticmethod
    def create_tweet(bool_as_string: str) -> bool:
        """Public Static Method create_tweet
        """
        if bool_as_string.lower() == 'true':
            return True
        elif bool_as_string.lower() == 'false':
            return False
        else:
            return False


    @staticmethod
    def is_valid_limit(headers: Dict[str, str]) -> bool:
        """Public Static Method is_valid_limit
        """
        is_valid = False

        if 'Limit' in headers:
            is_valid = (
                headers['Limit'].isdigit() and
                int(headers['Limit']) > 0 and
                int(headers['Limit']) <= 4
            )

        return is_valid
