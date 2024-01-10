"""Module for tests
"""

from datetime import datetime
from zoneinfo import ZoneInfo

import requests

from time import sleep


POLLS = [
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
    ]
]

COUNTER = 0
TWEET = 1

while True:
    COUNTER += 1

    print(f'Tweet parameter value is now {TWEET}')

    for poll_endpoint in POLLS[2]:
        
        URL = 'http://0.0.0.0:8080'
        HEADERS = { 'Poll-Endpoint': poll_endpoint, 'tweet': str(TWEET) }

        RESPONSE = requests.request(
            method='GET',
            url=URL,
            headers=HEADERS,
            timeout=10
        )

        now = datetime.now(tz=ZoneInfo(key='America/Sao_Paulo')).isoformat()

        request_msg = (
            f'\n{now}\n'
            f'Request #{COUNTER} for {poll_endpoint}\n'
            f'Status Code: {RESPONSE.status_code}\n'
            f'Tweet: {TWEET}\n')

        print(request_msg)
    
    sleep(300)
