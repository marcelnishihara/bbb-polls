"""Módulo de integração com a API do X para publicação de tweets.
"""

import os
import tweepy


class Twitter:
    """Gerencia autenticação e publicação na API do X (Twitter).
    """

    def __init__(self, data: dict) -> None:
        """Inicializa o cliente do X com credenciais de ambiente.

        Args:
            data (dict): Dados estruturados da enquete do Splash/UOL.
        """
        self.msg = ''
        self.data = data
        self.__client = tweepy.Client(
            consumer_key=os.environ[
                'TWITTER_CONSUMER_KEY'
            ],
            consumer_secret=os.environ[
                'TWITTER_CONSUMER_SECRET'
            ],
            access_token=os.environ[
                'TWITTER_ACCESS_TOKEN'
            ],
            access_token_secret=os.environ[
                'TWITTER_ACCESS_TOKEN_SECRET'
            ]
        )


    def compose_msg(
            self,
            today_is: dict,
            counter_limit: int = 3) -> None:
        """Formata o texto da enquete para publicação no X (Twitter).

        Monta a mensagem com o título da enquete, o ranking dos
        participantes até o limite, porcentagem dos demais, total
        de votos e timestamp. O resultado fica em `self.msg`.

        Args:
            today_is (dict): Dicionário com a data/hora atual e
                formatos.
            counter_limit (int, optional): Limite de participantes no
                ranking exibido. Padrão é 3.
        """
        self.msg = (
            f'Parcial da enquete @Splash_UOL #BBB26: '
            f'"{self.data["title"]}" #RedeBBB\n\n')

        firsts_three_percentage_sum = 0
        counter = 0

        for player in self.data['players']:
            player_percentage = format(player["percentage"], '.2f')

            if counter < counter_limit:
                self.msg += (
                    f'{player["position"]}º '
                    f'{player["name"]}: '
                    f'{player_percentage.replace(".", ",")}%\n'
                )

                firsts_three_percentage_sum += player['percentage']
                counter += 1

            else:
                break

        if len(self.data['players']) > counter_limit:
            rest = format(100-firsts_three_percentage_sum, '.2f')
            self.msg += f'\nOs demais somam {rest.replace(".", ",")}%'

        self.msg += (
            f'\nTotal de Votos: {self.data["totalOfVotes"]}\n')

        now = [
            today_is['now'].day,
            today_is['now'].month,
            today_is['now'].year,
            today_is['now'].hour,
            today_is['now'].minute,
            today_is['now'].second
        ]

        for index, value in enumerate(now):
            now[index] = f'0{value}' if value < 10 else value

        self.msg += (
            f'🕒 {now[0]}/'
            f'{now[1]}/'
            f'{now[2]} às '
            f'{now[3]}:'
            f'{now[4]}:'
            f'{now[5]}')


    def post(self) -> dict:
        """Publica a mensagem gerada no X através da biblioteca Tweepy.

        Returns:
            dict: Dicionário contendo o status ('success'), tamanho
                ('tweet_length'), dados ('response_data') ou erro
                ('error').
        """
        if not self.msg:
            return {
                'success': False, 
                'tweet_length': None, 
                'error': 'There\'s no tweet message'
            }

        tweet_length = len(self.msg)
        tweet_length_diff = 280 - tweet_length

        print(
            f'Tweet Length: {tweet_length} '
            f'of 280 characters ({tweet_length_diff} '
            'more characters allowed).'
        )

        if tweet_length <= 280:
            response = self.__client.create_tweet(text=self.msg)

            return {
                'success': True,
                'tweet_length': tweet_length,
                'response_data': response.data
            }

        else:
            return {
                'success': False,
                'tweet_length': tweet_length,
                'error': 'Tweet message is too long'
            }
