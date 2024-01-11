"""Module for the Class Helpers
"""

import pytz

from datetime import datetime


class Helpers:
    def __init__(self) -> None:
        pass


    @staticmethod
    def datetime() -> dict:
        """Static Method datetime
        """
        today_is = datetime.now(tz=pytz.timezone(zone='America/Sao_Paulo'))
        iso_format = today_is.isoformat()
        formatted = (
            iso_format
            .replace('-03:00', '')
            .replace('-', '_')
            .replace('T', '_')
            .replace(':', '_')
            .replace('.', '_'))
        
        return {
            'now': today_is,
            'formatted': formatted
        }


    @staticmethod
    def log(
        today_is: str,
        string_to_log: str,
        file_path: str = './',
        prefix: str = 'log',
        extension: str = 'json'
        ) -> None:
        """Static Method log
        """

        if file_path.endswith('/'):
            prefix = prefix.lower().replace(' ', '_')
            file_name = f'{file_path}{prefix}_{today_is}.{extension}'

            with open(file=file_name, mode='w', encoding='utf-8') as log_file: 
                log_file.write(string_to_log)
                log_file.close()

            print(f'Log file "{file_name}" Created!')

        else:
            raise ValueError('Missing dash character')
