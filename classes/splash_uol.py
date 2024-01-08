"""Module for the Class SplashUOL
"""

import html_to_json
import json
import re
import requests
import traceback


class SplashUOL:
    def __init__(self, poll_path: str) -> None:
        """Class SplashUOL
        """
        self.__poll_url_prefix = 'https://www.uol.com.br/splash/bbb/enquetes'
        self.__poll_url = ''
        self.__poll_page_html_code = ''
        self.__poll_data = {}

        if poll_path.startswith('/'):
            self.__poll_url = f'{self.__poll_url_prefix}{poll_path}'
        else:
            poll_url_does_not_start_with_dash_err = (
                'Class SplashUol Constructor: '
                'Missing dash character in the string passed '
                f'as poll_url parameter value: {poll_path}')

            raise ValueError(poll_url_does_not_start_with_dash_err)


    def get_poll_page_html_code(self) -> str:
        return self.__poll_page_html_code


    def get_poll_data(self) -> dict:
        return self.__poll_data


    def __get_poll_page_html_code(self) -> None:
        """Private Method __get_poll_url
        """
        poll_page = requests.request(
            method='GET',
            url=self.__poll_url,
            timeout=2)

        if poll_page.status_code == 200:
            self.__poll_page_html_code = poll_page.text
        else:
            poll_page_data_err = (
                'Splash/Uol poll page status code is '
                f'{poll_page.status_code}')

            raise Exception(poll_page_data_err)


    def __extract_poll_data(self) -> None:
        """Private Method __extract_poll_data
        """
        poll_html_code_to_json = html_to_json.convert(
            html_string=self.__poll_page_html_code)
        
        poll_data_root = (
            poll_html_code_to_json
            ['html']
            [0]
            ['body']
            [0]
            ['script']
            [0]
            ['_value'])
        
        initial_state_is_valid = re.search(
            pattern='window\.__INITIAL_STATE__=(.*)(\;\(function\(\).*)',
            string=poll_data_root)

        if initial_state_is_valid:
            poll_data_root = json.loads(s=initial_state_is_valid.group(1))

            poll_dict = poll_data_root['pinia']['poll']
            
            poll_title = re.search(
                pattern='(.*)\:(.*)',
                string=poll_dict['title'].strip()).group(2)

            self.__poll_data = { 
                'title': poll_title.strip(),
                'totalOfVotes':  poll_dict['votes'],
                'players': []
            }

            for player in poll_dict['result']:
                player_percentage = (
                    player['vote']
                    .replace(',', '.')
                    .replace('%', ''))

                self.__poll_data['players'].append({
                    'position': player['position'],
                    'id': player['id'],
                    'name': player['label'],
                    'percentage': float(player_percentage)
                })


    def run(self) -> None:
        """Method run
        """
        try:
            self.__get_poll_page_html_code()
            self.__extract_poll_data()

        except Exception:
            error_msg = (
                traceback.format_exc()
                .replace('\n', ' '))

            self.__poll_data = {}
            self.__poll_data['error'] = error_msg.strip()
