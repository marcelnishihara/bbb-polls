"""Módulo de funções auxiliares e utilitárias para data e logs.
"""

import pytz

from datetime import datetime


class Helpers:
    """Classe utilitária para data/hora e escrita de arquivos de log.
    """

    def __init__(self) -> None:
        """Inicializa a classe Helpers.
        """
        pass


    @staticmethod
    def datetime() -> dict:
        """Obtém a data/hora atual em SP formatada para arquivos.

        Returns:
            dict: Dicionário contendo o objeto datetime ('now') e a
                string formatada ('formatted').
        """
        today_is = datetime.now(
            tz=pytz.timezone(zone='America/Sao_Paulo')
        )
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
        """Grava uma string em arquivo nomeado com prefixo e data.

        Args:
            today_is (str): Timestamp formatado para compor o arquivo.
            string_to_log (str): Conteúdo textual a ser persistido.
            file_path (str, optional): Diretório de destino do arquivo.
                Deve terminar com '/'. Padrão é './'.
            prefix (str, optional): Prefixo do arquivo. Padrão é 'log'.
            extension (str, optional): Extensão sem o ponto. Padrão é
                'json'.

        Raises:
            ValueError: Se `file_path` não terminar com barra ('/').
        """

        if file_path.endswith('/'):
            prefix = prefix.lower().replace(' ', '_')
            file_name = f'{file_path}{prefix}_{today_is}.{extension}'

            with open(
                file=file_name,
                mode='w',
                encoding='utf-8'
            ) as log_file: 
                log_file.write(string_to_log)
                log_file.close()

            print(f'Log file "{file_name}" Created!')

        else:
            raise ValueError('Missing dash character')
