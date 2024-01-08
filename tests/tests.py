"""Module for tests
"""

import requests
from time import sleep


while True:

    POLLS = [
        '/2024/01/05/bbb-24---enquete-uol-ate-agora-qual-dos-participantes-anunciados-e-o-seu-preferido.htm',
        '/2024/01/07/bbb-24---enquete-uol-qual-das-6-mulheres-voce-quer-ver-entre-participantes.htm',
        '/2024/01/07/bbb-24---enquete-uol-quem-voce-quer-ver-entre-os-participantes.htm'
    ]


    for poll_endpoint in POLLS:
        URL = 'http://0.0.0.0:8080'
        HEADERS = { 'Poll-Endpoint': poll_endpoint }

        RESPONSE = requests.request(
            method='GET',
            url=URL,
            headers=HEADERS,
            timeout=10
        )

        print(RESPONSE.text) if RESPONSE.status_code == 200 else RESPONSE.status_code
        sleep(5)
    
    sleep(900)
