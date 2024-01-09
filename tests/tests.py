"""Module for tests
"""

import requests
from time import sleep


COUNTER = 0

while True:
    POLLS = [
        [
            '/2024/01/05/bbb-24---enquete-uol-ate-agora-qual-dos-participantes-anunciados-e-o-seu-preferido.htm',
            '/2024/01/07/bbb-24---enquete-uol-qual-das-6-mulheres-voce-quer-ver-entre-participantes.htm',
            '/2024/01/07/bbb-24---enquete-uol-quem-voce-quer-ver-entre-os-participantes.htm'
        ],
        [
            '/2024/01/08/bbb-24---enquete-uol-com-qual-dos-participantes-voce-teve-menos-afinidade.htm'
        ]
    ]

    COUNTER += 1

    for poll_endpoint in POLLS[1]:
        URL = 'http://0.0.0.0:8080'
        HEADERS = { 'Poll-Endpoint': poll_endpoint }

        RESPONSE = requests.request(
            method='GET',
            url=URL,
            headers=HEADERS,
            timeout=10
        )

        print(f'Request #{COUNTER} for {poll_endpoint}, Status Code: {RESPONSE.status_code}')
        sleep(120)

    sleep(900)
