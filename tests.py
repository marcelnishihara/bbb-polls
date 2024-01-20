"""Module for tests
"""

from classes.request_analysis import RequestAnalysis

import requests

from time import sleep


if __name__ == '__main__':
    polls = [
        [
            '/2024/01/05/bbb-24---enquete-uol-ate-agora-qual-dos-participantes-anunciados-e-o-seu-preferido.htm',
            '/2024/01/07/bbb-24---enquete-uol-qual-das-6-mulheres-voce-quer-ver-entre-participantes.htm',
            '/2024/01/07/bbb-24---enquete-uol-quem-voce-quer-ver-entre-os-participantes.htm'
        ],
        [
            '/2024/01/05/bbb-24---enquete-uol-ate-agora-qual-dos-participantes-anunciados-e-o-seu-preferido.htm',
            '/2024/01/08/bbb-24---enquete-uol-com-qual-dos-participantes-voce-teve-menos-afinidade.htm'
        ],
        [
            '/2024/01/09/bbb-24---enquete-uol-quem-voce-quer-fique-maycon-giovanna-ou-yasmin-brunet.htm'
        ],
        [
            '/2024/01/11/bbb-24---enquete-uol-quem-o-segundo-lider-vai-indicar-ao-paredao.htm',
        ],
        [
            '/2024/01/12/bbb-24---enquete-uol-quem-voce-quer-que-fique-na-casa.htm',
        ],
        [
            '/2024/01/15/bbb-24---enquete-uol-quem-voce-quer-que-fique-na-casa.htm'
        ],
        [
            '/2024/01/19/bbb-24---enquete-uol-quem-voce-quer-que-fique-na-casa-beatriz-davi-ou-pizane.htm'
        ]
    ]

    counter = 0

    while True:
        create_tweet = False

        if counter % 10 == 0:
            create_tweet = True

        print(f'Counter: {counter}. Tweet parameter value is now {create_tweet}')

        for poll_endpoint in polls[6]:
            client_uuid = RequestAnalysis.create_session_uuid_for_tests()

            headers = {
                'Endpoint': poll_endpoint,
                'Tweet': str(create_tweet),
                'Uuid': client_uuid
            }

            response = requests.request(
                method='GET',
                url='http://0.0.0.0:8080',
                headers=headers,
                timeout=10
            )

            response_msg = (
                f'Request Status Code: {response.status_code} | '
                f'Text: {response.text}')

            print(response_msg)
            sleep(1)

        sleep(119)
        counter += 1
