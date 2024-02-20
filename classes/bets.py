"""Module the Class Bets
"""

from classes.helpers import Helpers

import json
import requests


class Bets:
    def __init__(self) -> None:
        self.__url_database_path = './polls.json'
        self.__url = None


    def __get_url(
        self,
        platform: str = 'sportsbet',
        session: str = 'paredao',
        index: int = 0) -> None:
        with open(
            file=self.__url_database_path, 
            mode='r', 
            encoding='utf-8'
        ) as polls_file:
            url_database = json.loads(s=polls_file.read())
            polls_file.close()
            self.__url = url_database[platform][session][index]


    def __get_bets_page(self) -> None:
        """Private Method __get_poll_url
        """
        poll_page = requests.request(
            method='GET',
            url=self.__poll_url,
            timeout=2)


    def run(self) -> None:
        self.__get_url()
        print(self.__url_database)
