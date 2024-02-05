"""Module for the Class SplashUOL
"""

import html_to_json
import json
import re
import requests
import traceback


class SplashUOL:
    def __init__(self, today_is: str, poll_path: str) -> None:
        """Class SplashUOL
        """
        self.__today_is = today_is
        self.__poll_url_prefix = 'https://www.uol.com.br/splash/bbb/enquetes'
        self.__poll_url = f'{self.__poll_url_prefix}{poll_path}'
        self.__poll_page_html_code = ''
        self.__poll_html_code_to_json = {}
        self.__poll_data = {}


    def get_poll_page_html_code(self, as_json = False) -> str:
        if as_json:
            return self.__poll_html_code_to_json
        else:
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
        self.__poll_html_code_to_json = html_to_json.convert(
            html_string=self.__poll_page_html_code)

        self.__poll_html_code_to_json = json.loads(s=(
            self.__poll_html_code_to_json
            ['html']
            [0]
            ['body']
            [0]
            ['script']
            [7]
            ['_value']))

        self.__poll_data = {
            'todayIs': self.__today_is,
            'url': self.__poll_url,
            'title': self.__poll_html_code_to_json['poll']['title'],
            'totalOfVotes': self.__poll_html_code_to_json['poll']['votes'],
            'players': []
        }

        for player in self.__poll_html_code_to_json['poll']['result']:
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
