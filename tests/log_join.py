"""Script para agregação temporal de parciais de enquetes e
exportação para CSV (Flourish Bar Chart Race).
"""

import csv
import datetime
import json
import os


log_folder_path = './log'

log_files = list(filter(
    lambda f_name: (
        f_name.startswith('log_poll') and f_name.endswith('.json')
    ),
    os.listdir(path=log_folder_path)
))


def get_data(file: str) -> dict:
    """Lê e desserializa o conteúdo de um arquivo de log JSON.

    Args:
        file (str): Caminho para o arquivo de log JSON.

    Returns:
        dict: Dados da enquete carregados do JSON.
    """
    with open(file=file, mode='r', encoding='utf-8') as log_file:
        file_data = json.loads(log_file.read())
        log_file.close()

    return file_data

log_files_data = list(map(
    lambda log_file: get_data(f'{log_folder_path}/{log_file}'),
    log_files
))

poll_endpoint = (
    '/2025/03/31/'
    'bbb-25---enquete-uol-quem-voce-quer-eliminar-no-paredao.htm'
)

log_files_data = list(filter(
    lambda data: (
        'url' in data and
        poll_endpoint in data['url'] and
        data['players'] != []
    ),
    log_files_data
))

data = sorted(
    log_files_data,
    key=lambda partial: partial['todayIs']
)

print(len(data))

csv_file = "flourish_bar_chart_race.csv"

def format_today_is(date_str):
    """Converte o timestamp do log para formato legível.

    Args:
        date_str (str): Timestamp ('AAAA_MM_DD_HH_MM_SS').

    Returns:
        str: Data e hora formatadas ('DD/MM/AAAA HH:MM').
    """
    date_obj = datetime.datetime.strptime(
        date_str[:19],
        "%Y_%m_%d_%H_%M_%S"
    )
    return date_obj.strftime("%d/%m/%Y %H:%M")

header = (
    ["participantes", "imagem_url"] +
    [format_today_is(entry["todayIs"]) for entry in data]
)

consolidated_data = {}

for entry in data:
    todayIs = format_today_is(entry["todayIs"])

    if len(entry["players"]) >= 2:
        for player in entry["players"]:
            name = player["name"]
            percentage = player["percentage"]

            if name not in consolidated_data:
                consolidated_data[name] = {"imagem_url": ""}

            consolidated_data[name][todayIs] = percentage

with open(
    csv_file,
    mode="w",
    encoding="utf-8",
    newline=""
) as file:
    writer = csv.writer(file)    
    writer.writerow(header)

    for participant, values in consolidated_data.items():
        row = [participant, values["imagem_url"]]
        
        for todayIs in header[2:]:
            row.append(values.get(todayIs, ""))

        writer.writerow(row)

print(f"Arquivo CSV '{csv_file}' criado com sucesso.")
