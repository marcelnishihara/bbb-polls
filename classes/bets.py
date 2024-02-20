"""Module the Class Bets
"""

from classes.helpers import Helpers

import html_to_json
import json
import requests


class Bets:
    def __init__(self) -> None:
        self.__url_database_path = './polls.json'
        self.__url = None
        self.__html_to_json = {}


    def __get_url(
        self,
        platform: str = 'bet365',
        session: str = 'paredao',
        index: int = 0) -> None:
        with open(
            file=self.__url_database_path, 
            mode='r', 
            encoding='utf-8'
        ) as polls_file:
            url_database = json.loads(s=polls_file.read())
            polls_file.close()
            self.__url = (
                f'{url_database["bets"][platform]["urlPrefix"]}'
                f'{url_database["bets"][platform][session][index]}')


    def __request(self) -> None:
        bet_html_string = requests.request(
            method='GET',
            url=self.__url,
            timeout=2)
      
        self.__html_to_json = html_to_json.convert(
            html_string=bet_html_string.text
        )


    def run(self) -> None:
        self.__get_url()
        self.__request()

        today_is = Helpers.datetime()

        Helpers.log(
            today_is=today_is['formatted'],
            string_to_log=json.dumps(obj=self.__html_to_json, indent=4),
            file_path='./log/',
            prefix='__log_bets'
        )
