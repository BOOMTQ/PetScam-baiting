import requests
import json
from datetime import datetime, timedelta
from os import listdir
from os.path import isfile, join
from secret import API_KEY, API_BASE_URL, MAIL_SAVE_DIR
from email.utils import parsedate_to_datetime
import time

logs_url = f'{API_BASE_URL}/events'

local_path = 'D:/UoB/UG/大三/individual project/Petscam-baiting/emails/queued/'
handled_email_path = 'D:/UoB/UG/大三/individual project/Petscam-baiting/emails/handled/'

# Get the current UTC date and time
now_utc = datetime.utcnow()

# Set the time to midnight (00:00:00) to get the start of today in UTC
today_utc = datetime.combine(now_utc.date(), datetime.min.time())

# Subtract one day to get the start of yesterday in UTC
day_before_yesterday_utc = today_utc - timedelta(days=2)

# Format the date as a string in RFC 2822 format with the UTC offset, include emails in day1, day2 and day3
two_days_ago = day_before_yesterday_utc.strftime('%a, %d %b %Y %H:%M:%S +0000')


downloaded_emails = [f for f in listdir(local_path) if isfile(join(local_path, f))]
handled_emails = [f for f in listdir(handled_email_path) if isfile(join(handled_email_path, f))]


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


def get_mailgun_logs():

    response = requests.get(
        logs_url,
        auth=('api', API_KEY),
        params={"begin": two_days_ago,
                "ascending": "yes",
                "limit": 100,
                "event": "stored"}
    )

    if response.status_code == 200:
        logs_data = response.json()
        for item in logs_data['items']:
            # Assume full_email is the full email data retrieved from Mailgun
            full_email = requests.get(item['storage']['url'], auth=('api', API_KEY)).json()

            # Extract the date from the email and convert it to a Unix timestamp
            date_header = full_email.get('Date', '')
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

                    # write the email to a file
                    with open(local_path + filename, 'w') as email_file:
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
