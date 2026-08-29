"""Módulo principal da Google Cloud Function.

Coordena a validação de requisições, a extração de dados de enquetes
do Splash/UOL, o registro de logs e a geração de mensagens para tweets.
"""

from classes.helpers import Helpers
from classes.request_analysis import RequestAnalysis
from classes.splash_uol import SplashUOL
from classes.twitter import Twitter

import flask
import json

from traceback import format_exc


def process(request: flask.Request, today_is: dict) -> tuple:
    """Processa a extração dos dados e gerencia logs e mensagens.

    Instancia o extrator do Splash/UOL, salva os dados coletados em
    formato JSON, avalia se deve preparar a mensagem de tweet e
    realiza o log do texto gerado.

    Args:
        request (flask.Request): Objeto da requisição HTTP recebida
            contendo os cabeçalhos necessários ('Endpoint', 'Tweet',
            opcionalmente 'Limit').
        today_is (dict): Dicionário contendo instâncias e formatos da
            data/hora atual.

    Returns:
        tuple: Tupla com a mensagem de status e o código HTTP.
    """
    splash_uol = SplashUOL(
        today_is=today_is['formatted'],
        poll_path=request.headers['Endpoint']
    )

    splash_uol.run()
    poll_data = splash_uol.get_poll_data()

    Helpers.log(
        today_is=today_is['formatted'],
        string_to_log=json.dumps(obj=poll_data, indent=4),
        file_path='./log/',
        prefix='log_poll'
    )

    create_tweet = RequestAnalysis.create_tweet(
        bool_as_string=request.headers['Tweet']
    )

    tuple_to_return = ('Poll Data Logged', 200)

    if create_tweet:
        if RequestAnalysis.is_valid_limit(headers=request.headers):
            counter_limit = int(request.headers['Limit'])
        else:
            counter_limit = 3

        twitter_session = Twitter(poll_data)
        twitter_session.compose_msg(
            today_is=today_is,
            counter_limit=counter_limit
        )

        Helpers.log(
            today_is=today_is['formatted'],
            string_to_log=twitter_session.msg,
            file_path='./tweets/',
            prefix='log_tweet_msg',
            extension='txt'
        )

        return ('Tweet Message Logged', 200)

        '''
        tweet_data = twitter_session.post()

        Helpers.log(
            today_is=today_is['formatted'],
            string_to_log=json.dumps(obj=tweet_data, indent=4),
            file_path='./log/',
            prefix='log_tweet_data'
        )

        if tweet_data['success']:
            tuple_to_return = ('Tweet Created', 201)
        else:
            tuple_to_return = (
                tweet_data['error'],
                tweet_data['status_code']
            )
        '''

    return tuple_to_return


def main(request) -> tuple:
    """Ponto de entrada (entry point) da Cloud Function.

    Valida os cabeçalhos de segurança e integridade da requisição.
    Em caso de sucesso, encaminha para o processamento; caso contrário,
    registra o log de erro e retorna Bad Request (HTTP 400).

    Args:
        request (flask.Request): Objeto da requisição HTTP do
            Flask/Cloud Functions.

    Returns:
        tuple: Tupla contendo o corpo da resposta e o status code HTTP.
    """
    today_is = Helpers.datetime()

    is_valid_request, explanation = RequestAnalysis.is_valid_request(
        headers=request.headers
    )

    try:
        if is_valid_request:
            tuple_to_return = process(
                request=request,
                today_is=today_is
            )
            return tuple_to_return

        else:
            bad_request_json = json.dumps(
                obj={
                    'badRequest': True,
                    'todayIs': today_is['formatted'],
                    'explanation': explanation
                },
                indent=4
            )

            Helpers.log(
                today_is=today_is['formatted'],
                string_to_log=bad_request_json,
                file_path='./log/',
                prefix='log_bad_request'
            )

            return (bad_request_json, 400)

    except Exception:
        return (format_exc().replace('\n', ' '), 500)
