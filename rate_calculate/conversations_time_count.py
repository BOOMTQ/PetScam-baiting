import json
import re
from pathlib import Path

from secret import MAIL_ARCHIVE_DIR, MODEL_HISTORY_PATH

txt_archive = MAIL_ARCHIVE_DIR
history_record = MODEL_HISTORY_PATH


def count_time(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    inbound_matches = re.findall(r"# Inbound\nFROM:.*?\n.*?TIME: (\d+)", content, re.DOTALL)
    inbound_timestamps = [int(match) for match in inbound_matches]

    if inbound_timestamps:
        first_timestamp = inbound_timestamps[0]
        last_timestamp = inbound_timestamps[-1]
        time_diff_hours = (last_timestamp - first_timestamp) / 3600.0
        return len(inbound_timestamps), time_diff_hours
    else:
        return 0, 0


def update_history(email, new_inbound_count, time_diff_hours, json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        history_data = json.load(file)

    email_data = history_data['scam_emails'].get(email, {})
    current_inbound_count = email_data.get('inbound_count', 0)

    time_diff_hours = round(time_diff_hours, 2)

    if new_inbound_count > current_inbound_count or 'time_diff_hours' not in email_data or new_inbound_count == 1:
        history_data['scam_emails'][email] = {
            'has_replied': True,
            'sol_used': email_data.get('sol_used', ''),
            'inbound_count': new_inbound_count,
            'time_diff_hours': time_diff_hours
        }
    else:
        print(f"No history update needed for {email}.")

    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(history_data, file, indent=4)


def main():
    txt_files = Path(txt_archive).glob('*.txt')
    for txt_file in txt_files:
        email = txt_file.stem
        new_inbound_count, time_diff_hours = count_time(txt_file)
        update_history(email, new_inbound_count, time_diff_hours, history_record)


if __name__ == '__main__':
    main()


