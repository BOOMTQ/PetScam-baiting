import requests

from secret import API_KEY, API_BASE_URL

with open("mailgun/template.html", "r") as f:
    template = f.read()


# Send email by Mailgun API

def send_email(username, address, target, subject, text):
    if type(target) == str:
        target = [target]

    print(f"Send an email from {address} to {target}")

    res = requests.post(
        f"{API_BASE_URL}/messages",
        auth=("api", API_KEY),
        data={"from": f"{username} <{address}>",
              "to": target,
              "subject": str(subject),
              "html": template.replace("{{{content}}}", text).replace("\n", "<br>")})
    if not ("Queued." in res.text):
        print(f"Failed to send, {res.text}")
        return False
    return True


if __name__ == '__main__':
    print(send_email("HelloTester", "su777@malabaka.social", "77lovesm@gmail.com", "==Test==",
                     "Test these fucking stuff"))
