"""Module for the Class Twitter
"""

import os
import tweepy


class Twitter:
    '''Class Twitter
    '''

    def __init__(self, data: dict) -> None:
        self.msg = ''
        self.data = data
        self.__client = tweepy.Client(
            consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
            consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
            access_token=os.environ['TWITTER_ACCESS_TOKEN'],
            access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])


    def __compose_msg(
            self,
            today_is: dict,
            poll_number_of_players: int,
            counter_limit: int = 3) -> None:
        '''Method __compose_msg
        '''
        self.msg = (
            f'Parcial da enquete @Splash_UOL #BBB25: '
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

        if poll_number_of_players > counter_limit:
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


    def post(self, today_is: dict, counter_limit: int = 3) -> dict:
        '''Method post
        '''
        self.__compose_msg(
            counter_limit=counter_limit,
            poll_number_of_players=len(self.data['players']),
            today_is=today_is
        )

        tweet_length = len(self.msg)
        print(f'Tweet Length: {tweet_length} characters')

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
