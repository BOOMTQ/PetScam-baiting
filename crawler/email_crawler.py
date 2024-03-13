import requests
import json
import time
from datetime import datetime, timedelta
from os import listdir
from os.path import isfile, join

from archiver import archive
from secret import API_KEY, API_BASE_URL
from email.utils import parsedate_to_datetime
from secret import CRAWLER_PROG_DIR, ADDR_SOL_PATH, MAIL_HANDLED_DIR, MAIL_SAVE_DIR

logs_url = f'{API_BASE_URL}/events'

# Get the current UTC date and time
now_utc = datetime.utcnow()

# Set the time to midnight (00:00:00) to get the start of today in UTC
today_utc = datetime.combine(now_utc.date(), datetime.min.time())

# Subtract one day to get the start of yesterday in UTC
day_before_yesterday_utc = today_utc - timedelta(days=2)

# Format the date as a string in RFC 2822 format with the UTC offset, include emails in day1, day2 and day3
two_days_ago = day_before_yesterday_utc.strftime('%a, %d %b %Y %H:%M:%S +0000')

downloaded_emails = [f for f in listdir(MAIL_SAVE_DIR) if isfile(join(MAIL_SAVE_DIR, f))]
handled_emails = [f for f in listdir(MAIL_HANDLED_DIR) if isfile(join(MAIL_HANDLED_DIR, f))]


def format_email(email_data):
    from_email = email_data.get('From', '')
    if '<' in from_email and '>' in from_email:
        from_email = from_email.split('<')[1].split('>')[0]

    bait_email = email_data.get('To', '')
    if '<' in bait_email and '>' in bait_email:
        bait_email = bait_email.split('<')[1].split('>')[0]

    # Format the email data structure to match corn.py
    formatted_email = {
        'content': email_data.get('body-plain', ''),
        'title': email_data.get('subject', ''),
        'from': from_email,
        'bait_email': bait_email,
    }

    return formatted_email


def update_record(formatted_email):
    with open(CRAWLER_PROG_DIR, 'r') as f:
        cache_data = json.load(f)

    bait_email = formatted_email['bait_email']
    scam_email = formatted_email['from']

    record_updated = False
    for cache in cache_data:
        if cache['bait_email'] == bait_email:
            record = {
                "bait_email": bait_email,
                "sol": cache.get('sol', ''),
                "scam_email": scam_email,
                "username": cache.get('username', '')
            }
            # Update record.json
            try:
                if isfile(ADDR_SOL_PATH):
                    with open(ADDR_SOL_PATH, 'r') as record_file:
                        records = json.load(record_file)
                else:
                    records = {}

                # Check if the record for this bait_email already exists
                existing_record = records.get(record['bait_email'])
                if existing_record:
                    # if the record exists, do not re-store it
                    print(f"Record for bait email: {record['bait_email']} already exists.")
                else:
                    # Otherwise, add the new record
                    records[record['bait_email']] = {
                        "sol": record.get('sol', ''),
                        "to": record.get('scam_email', ''),
                        "username": record.get('username', '')
                    }
                    print(f"Added new record for bait email: {record['bait_email']}")

                # Write new records back to the file.
                with open(ADDR_SOL_PATH, 'w') as record_file:
                    json.dump(records, record_file, indent=4)

            except Exception as e:
                print(f"An error occurred while updating the records: {e}")
            record_updated = True
            break

    if not record_updated:
        print(f"No matching cache found for bait email: {bait_email}")


def get_mailgun_logs():
    response = requests.get(
        logs_url,
        auth=('api', API_KEY),
        params={"begin": two_days_ago,
                "ascending": "yes",
                "limit": 200,
                "event": "stored"}
    )

    if response.status_code == 200:
        logs_data = response.json()
        for item in logs_data['items']:
            # Assume full_email is the full email data retrieved from Mailgun
            full_email = requests.get(item['storage']['url'], auth=('api', API_KEY)).json()

            # Extract the date from the email and convert it to a Unix timestamp
            date_header = full_email.get('Date', '')
            timestamp = int(time.time())
            if date_header:
                email_datetime = parsedate_to_datetime(date_header)
                timestamp = int(time.mktime(email_datetime.timetuple()))
                filename = f"mailgun_email_{timestamp}.json"
            else:
                filename = f"mailgun_email_{int(time.time())}.json"

            # Only save new emails that haven't been downloaded before
            if filename not in downloaded_emails and filename not in handled_emails:
                # Retrieve stored emails from Mailgun
                stored_response = requests.get(
                    item['storage']['url'],
                    auth=('api', API_KEY)
                )

                if stored_response.status_code == 200:
                    full_email = stored_response.json()

                    stored_email = format_email(full_email)
                    scam_email = stored_email.get('from')
                    bait_email = stored_email.get('bait_email')
                    subject = stored_email.get('title')
                    body = stored_email.get('content')

                    update_record(stored_email)
                    archive(True, scam_email, bait_email, subject, body, timestamp)

                    # write the email to a file and save it to MAIL_SAVE_DIR
                    with open(MAIL_SAVE_DIR + filename, 'w') as email_file:
                        json.dump(stored_email, email_file, indent=4)
                    print(f"Email saved to {filename}")
                else:
                    print(f"Failed to retrieve stored email. Status code: {stored_response.status_code}")
            else:
                print(f"This email has been downloaded, please wait for more newest incoming emails")
    else:
        print(f"Failed to retrieve logs. Status code: {response.status_code}")
        print(f"Response content: {response.content.decode()}")


def main():
    get_mailgun_logs()


if __name__ == '__main__':
    main()
