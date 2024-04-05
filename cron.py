import json
import os
import shutil
import sys
import time
import traceback

import tiktoken
import mailgun
import responder
import solution_manager
from rate_calculate.calculator import email_reply_rate
from secret import MAIL_SAVE_DIR, MAIL_HANDLED_DIR
from archiver import archive


def main(crawl=True):
    start_time = int(time.time())
    attempted_replies = 0
    successful_replies = 0

    if crawl:
        pass

    # Handle incoming emails
    email_filenames = os.listdir(MAIL_SAVE_DIR)
    count = 0

    for email_filename in email_filenames:
        if count < 201:
            try:
                print(f"Handling {email_filename}")
                email_path = os.path.join(MAIL_SAVE_DIR, email_filename)
                with open(email_path, "r", encoding="utf8") as f:
                    email_obj = json.load(f)

                text = email_obj["content"]
                attempted_replies += 1

                encoding = tiktoken.encoding_for_model("gpt-4-0125-preview")
                num_tokens = len(encoding.encode(text))
                if num_tokens > 29000:
                    print("This email is too long")
                    # os.remove(email_path)
                    continue

                subject = str(email_obj["title"])
                if not subject.startswith("Re:"):
                    subject = "Re: " + subject
                scam_email = email_obj["from"]
                bait_email = email_obj["bait_email"]
                stored_info = solution_manager.get_stored_info(bait_email, scam_email)

                if stored_info is None:
                    print(f"Cannot found replier for {bait_email}")
                    # os.remove(email_path)
                    continue

                print(f"Found selected replier {stored_info.sol}")
                replier = responder.get_replier_by_name(stored_info.sol)
                responder.update_replier_history(scam_email, stored_info.sol)

                if replier is None:
                    print("Replier Sol_name not found")
                    # os.remove(email_path)
                    continue

                try:
                    res_text = replier.get_reply(text)
                except Exception as e:
                    print("GENERATING ERROR")
                    print(e)
                    print(traceback.format_exc())
                    print("Due to CUDA Error, stopping whole sequence")
                    return

                # Add Signature
                res_text += f"\n\nBest wishes,\n{stored_info.username}"
                timestamp = int(time.time())

                send_result = mailgun.send_email(stored_info.username, stored_info.addr, scam_email, subject, res_text)
                if send_result:
                    successful_replies += 1
                    print(f"Successfully sent response to {scam_email}")
                    count += 1

                    # Move from queued to handled dir
                    if not os.path.exists(MAIL_HANDLED_DIR):
                        os.makedirs(MAIL_HANDLED_DIR)
                    shutil.move(email_path, os.path.join(MAIL_HANDLED_DIR, email_filename))

                    archive(False, scam_email, bait_email, subject, res_text, timestamp)
            except Exception as e:
                print(e)
                print(traceback.format_exc())
        else:
            print("Too many emails sent, try the rest later.")
            break
    else:
        print("No more emails to reply")

    success_rate = email_reply_rate("email_replier", successful_replies, attempted_replies, start_time)
    print(f"Email reply success rate: {success_rate}%")


if __name__ == '__main__':
    if os.path.exists("./lock"):
        quit(-1)

    with open("./lock", "w") as f:
        f.write("Running")

    arg_crawl = not ("--no-crawl" in sys.argv)
    main(crawl=arg_crawl)
    os.remove("./lock")
