from secret import MAIL_ARCHIVE_DIR
import os


def extract_latest_email_content(body):
    history_separators = ["\nFrom:", "\nSent:", "\r\n>\r\n>"]
    for sep in history_separators:
        parts = body.split(sep, 1)
        if len(parts) > 1:
            body = parts[0].strip()
            break
    return body


def archive(is_inbound, scam_email, bait_email, subject, body, timestamp):
    latest_body = extract_latest_email_content(body)

    archive_name = scam_email + ".txt"
    archive_content = \
        f'# {"Inbound" if is_inbound else "Outbound"}\n' \
        f'FROM: {scam_email if is_inbound else bait_email}\n' \
        f'To: {bait_email if is_inbound else scam_email}\n' \
        f'SUBJECT: {subject}\n' \
        f'TIME: {timestamp}\n' \
        f'\n{latest_body}\n'

    if not os.path.exists(MAIL_ARCHIVE_DIR):
        os.makedirs(MAIL_ARCHIVE_DIR)

    with open(f"{MAIL_ARCHIVE_DIR}/{archive_name}", "a", encoding="utf8") as f:
        f.write(archive_content)

    history_filename = scam_email + ".his"
    if is_inbound:
        his_content = "[scam_start]\n" + latest_body + "\n[scam_end]\n"
    else:
        his_content = "[bait_start]\n" + latest_body + "\n[bait_end]\n"

    with open(os.path.join(MAIL_ARCHIVE_DIR, history_filename), "a", encoding="utf8") as f:
        f.write(his_content)

    print(f"Archive for {scam_email} completed")
