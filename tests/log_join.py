import csv
import datetime
import json
import os


log_folder_path = './log'

log_files = list(filter(
    lambda log_file_name: log_file_name.startswith('log_poll') and log_file_name.endswith('.json'),
    os.listdir(path=log_folder_path)
))


def get_data(file: str) -> dict:
    with open(file=file, mode='r', encoding='utf-8') as log_file:
        file_data = json.loads(log_file.read())
        log_file.close()

    return file_data

log_files_data = list(map(
    lambda log_file: get_data(f'{log_folder_path}/{log_file}'),
    log_files
))

poll_endpoint = '/2025/01/20/bbb-25---enquete-uol-primeiro-paredao.htm'

log_files_data = list(filter(
    lambda data: 'url' in data and poll_endpoint in data['url'] and data['players'] != [],
    log_files_data
))

data = sorted(log_files_data, key=lambda partial: partial['todayIs'])

print(len(data))

csv_file = "flourish_bar_chart_race_0332.csv"

def format_today_is(date_str):
    date_obj = datetime.datetime.strptime(date_str[:19], "%Y_%m_%d_%H_%M_%S")
    return date_obj.strftime("%d/%m/%Y %H:%M")

header = ["participantes", "imagem_url"] + [format_today_is(entry["todayIs"]) for entry in data]

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

with open(csv_file, mode="w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)    
    writer.writerow(header)

    for participant, values in consolidated_data.items():
        row = [participant, values["imagem_url"]]
        
        for todayIs in header[2:]:
            row.append(values.get(todayIs, ""))

        writer.writerow(row)

print(f"Arquivo CSV '{csv_file}' criado com sucesso.")
