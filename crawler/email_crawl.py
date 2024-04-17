import requests
import json

from datetime import datetime, timedelta
from os import listdir
from os.path import isfile, join

from archiver import archive
from secret import API_KEY, API_BASE_URL

from secret import CRAWLER_PROG_DIR, ADDR_SOL_PATH, MAIL_HANDLED_DIR, MAIL_SAVE_DIR
import pytz

logs_url = f'{API_BASE_URL}/events'
gmt_zone = pytz.timezone('GMT')
bst_zone = pytz.timezone('Europe/London')

# gmt and utc are the same in winter
now_utc = datetime.utcnow()
now_gmt = gmt_zone.localize(now_utc)

dst_now = now_gmt.astimezone(bst_zone).dst() != timedelta(0)

# check if now is bst_zone(3.31-10.27)
if dst_now:
    # transform gmt to bst
    now_bst = now_gmt.astimezone(bst_zone)
    today_bst = now_bst.replace(hour=0, minute=0, second=0, microsecond=0)
    day_before_today_bst = today_bst - timedelta(days=1)
    # RFC 2822 format with the BST offset
    one_day_ago = day_before_today_bst.strftime('%a, %d %b %Y %H:%M:%S +0100')
else:
    today_gmt = now_gmt.replace(hour=0, minute=0, second=0, microsecond=0)
    day_before_today_gmt = today_gmt - timedelta(days=1)
    # RFC 2822 format with the GMT offset
    one_day_ago = day_before_today_gmt.strftime('%a, %d %b %Y %H:%M:%S +0000')


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


def update_record(formatted_email, timestamp):
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
                "username": cache.get('username', ''),
                "first_timestamp": timestamp
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
                        "username": record.get('username', ''),
                        "first_timestamp": timestamp
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


def get_logs():
    response = requests.get(
        logs_url,
        auth=('api', API_KEY),
        params={"begin": one_day_ago,
                "ascending": "yes",
                "limit": 200,
                "event": "stored"}
    )

    if response.status_code == 200:
        logs_data = response.json()
        for item in logs_data['items']:
            # Use the timestamp from the Mailgun event log
            mailgun_timestamp = item['timestamp']
            # Convert Mailgun's timestamp (which is in UTC seconds) to a Unix timestamp
            timestamp = int(mailgun_timestamp)
            filename = f"mailgun_email_{timestamp}.json"

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

                    # Pass the Mailgun timestamp to the update_record function
                    update_record(stored_email, timestamp)
                    archive(True, scam_email, bait_email, subject, body, timestamp)

                    # write the email to a file and save it to MAIL_SAVE_DIR
                    with open(join(MAIL_SAVE_DIR, filename), 'w') as email_file:
                        json.dump(stored_email, email_file, indent=4)
                    print(f"Email saved to {filename}")
                else:
                    print(f"Failed to retrieve stored email. Status code: {stored_response.status_code}")
            else:
                print(f"Email_{timestamp} is in the queue or has been handled. Skipping...")
    else:
        print(f"Failed to retrieve logs. Status code: {response.status_code}")
        print(f"Response content: {response.content.decode()}")


def main():
    get_logs()


if __name__ == '__main__':
    main()
