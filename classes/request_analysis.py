"""Módulo de validação de requisições, segurança e parâmetros HTTP.
"""

from classes.helpers import Helpers

import os
import requests
import uuid

from typing import Dict, List, Union, Tuple


class RequestAnalysis:
    """Validação e autenticação das requisições recebidas.
    """

    @staticmethod
    def __create_uuid_name_parameter() -> str:
        """Gera a string base temporal para o UUID da sessão.

        Returns:
            str: Data e hora no formato 'AAAA_MM_DD_HH_MM'.
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
        """Gera um UUID v5 baseado no namespace de ambiente.

        Args:
            uuid_name (str): Nome base temporal para a sessão.

        Returns:
            str: String representativa do UUID v5 gerado.
        """
        namespace = uuid.UUID(hex=os.environ['UUID'])
        return str(uuid.uuid5(namespace=namespace, name=uuid_name))


    @staticmethod
    def __is_valid_endpoint(endpoint: str) -> bool:
        """Verifica se o endpoint é acessível e retorna HTTP 200.

        Args:
            endpoint (str): Caminho relativo da enquete no Splash/UOL.

        Returns:
            bool: True se começar com '/' e retornar 200, False se não.
        """
        poll_url_prefix = (
            'https://www.uol.com.br/splash/bbb/enquetes'
        )
        
        if endpoint.startswith('/'):
            url = f'{poll_url_prefix}{endpoint}'
            response = requests.request(
                method='GET',
                url=url,
                timeout=2
            )
            return True if response.status_code == 200 else False
        else:
            return False


    @staticmethod
    def create_session_uuid_for_tests() -> str:
        """Gera o UUID temporal de sessão para scripts de teste.

        Returns:
            str: UUID v5 válido para o minuto corrente.
        """
        uuid_name = RequestAnalysis.__create_uuid_name_parameter()
        return RequestAnalysis.__create_session_uuid(
            uuid_name=uuid_name
        )


    @staticmethod
    def is_valid_request(
        headers: Dict[str, str]
        ) -> Tuple[bool, Union[None, List]]:
        """Valida autenticação, endpoint e parâmetros da requisição.

        Args:
            headers (Dict[str, str]): Cabeçalhos HTTP recebidos.

        Returns:
            Tuple[bool, Union[None, List]]: Tupla com booleano de
                validade e lista de erros caso inválida (ou None).
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

        return (
            (True, None) if is_valid_request
            else (False, request_not_valid)
        )


    @staticmethod
    def create_tweet(bool_as_string: str) -> bool:
        """Converte parâmetro string de tweet em booleano.

        Args:
            bool_as_string (str): Valor em string ('true'/'false').

        Returns:
            bool: True se for 'true', False caso contrário.
        """
        if bool_as_string.lower() == 'true':
            return True
        elif bool_as_string.lower() == 'false':
            return False
        else:
            return False


    @staticmethod
    def is_valid_limit(headers: Dict[str, str]) -> bool:
        """Verifica se 'Limit' é inteiro válido entre 1 e 4.

        Args:
            headers (Dict[str, str]): Dicionário de cabeçalhos HTTP.

        Returns:
            bool: True se 'Limit' for inteiro em [1, 4], False se não.
        """
        is_valid = False

        if 'Limit' in headers:
            is_valid = (
                headers['Limit'].isdigit() and
                int(headers['Limit']) > 0 and
                int(headers['Limit']) <= 4
            )

        return is_valid
