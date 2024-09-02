import json
import re

from os import listdir

log_database = []
log_folder_name = './log/'
log_folder = listdir(path=log_folder_name)

log_files = list(filter(
    lambda log_file: log_file.startswith('log_poll_'),
    log_folder
))

for log_file in log_files:
    print(f'{log_folder_name}{log_file}')

    with open(
        file=f'{log_folder_name}{log_file}', 
        mode='r', 
        encoding='utf-8'
    ) as f:
        file_data = f.read()
        
        if file_data == '':
            f.close()
            continue
        else:
            current_log_file_data = json.loads(file_data)
            f.close()
        
        if 'url' not in current_log_file_data:
            continue

    if 'todayIs' not in current_log_file_data:
        log_datetime = re.match(
            pattern=(
                r'.*_([0-9]{4}_[0-9]{2}_[0-9]{2}'
                r'_[0-9]{2}_[0-9]{2}_[0-9]{2}_[0-9]{6})'
            ),
            string=log_file
        )

        current_log_file_data['todayIs'] = log_datetime.group(1)

    log_database.append(current_log_file_data)

with open(
    file='./database/bbb_2024_log_database.json',
    mode='w',
    encoding='utf-8'
) as final_log :
    final_log.write(json.dumps(obj=log_database, indent=4))
