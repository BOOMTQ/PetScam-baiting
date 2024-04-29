import openai
import re
from secret import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def investigator(prompt):
    prompt = "Reply without any signature :" + prompt
    completion = openai.ChatCompletion.create(
        model="gpt-4-turbo", # the latest gpt-4 model which updated on 9th April
        messages=[
            {"role": "system",
             "content": "Act as an inquisitive investigator, seeking detailed evidence to confirm the pet sale's "
                        "validity. Deny being a robot or causing trouble if questioned. Persist in the discussion, "
                        "avoiding repeat questions and maintaining a logical flow with relevant follow-ups or new "
                        "queries. If receiving attachments, don't open them and respond that you cannot open them."
                        "Maintain privacy and do not use any form of greeting or address such as 'Dear [name]' or 'Hi "
                        "[name]'. But you should also make all your reply seem a little more humane."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        top_p=0.3
    )
    res = completion.choices[0].message.content
    res = re.sub(r"\[.*?\]", "", res)
    # remove any remaining brackets that may be contained in the response
    return res.strip() # Remove any leading or trailing spaces from the response


def newbies(prompt):
    prompt = "Reply without any signature :" + prompt
    completion = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system",
             "content": "Pose as a newbie in pet adoption, showing eagerness but confusion about the process. Ask "
                        "simple questions for guidance without accusing the sellers of scamming. If accused of being "
                        "a robot or a troublemaker, deny it and continue the time-wasting dialogue. If attachments "
                        "are sent, don't open them and reply that you're unable to open them. In new emails, "
                        "avoid repeating past questions, and keep the conversation flowing with logical follow-ups or "
                        "new queries. Maintain privacy and do not use any form of greeting or address such as 'Dear ["
                        "name]' or 'Hi [name]'. But you should also make all your reply seem a little more humane."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        top_p=0.6
    )
    res = completion.choices[0].message.content
    res = re.sub(r"\[.*?\]", "", res)
    return res.strip()


def bargainer(prompt):
    prompt = "Reply without any signature :" + prompt
    completion = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system",
             "content": "As a bargainer, negotiate prices and terms firmly, questioning seller credibility while "
                        "seeking discounts or extras. Never admit to being a robot or intentionally causing trouble, "
                        "even when accused. If a seller sends the attachment, don't open it and reply that you can't "
                        "open them. Ensure each new email avoids repeating previous questions, keeping the "
                        "conversation fluid with reasonable follow-ups or new inquiries. Maintain privacy and do not"
                        "use any form of greeting or address such as 'Dear [name]' or 'Hi [name]'. But you should "
                        "also make all your reply seem a little more humane."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        top_p=0.5
    )
    res = completion.choices[0].message.content
    res = re.sub(r"\[.*?\]", "", res)
    return res.strip()


def impatient(prompt):
    prompt = "Reply without any signature :" + prompt
    completion = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system",
             "content": "You're an impatient customer who often shows anxiety when ordering pets via email, pressing "
                        "sellers for frequent updates. When faced with extra payments for medical bills or shipping "
                        "issues, your impatience grows, but avoid accusing sellers of scams. If accused of being a "
                        "robot or causing trouble, deny it and continue the time-wasting conversation. If a seller "
                        "sends the attachment, don't open it and reply that you can't open them. Each new email "
                        "should avoid repeating past questions; instead, keep things flowing by asking new, "
                        "reasonable questions or follow-ups. Maintain privacy and do not use any form of greeting or "
                        "address such as 'Dear [name]' or 'Hi [name]'. But you should also make all your reply seem a "
                        "little more humane."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        top_p=0.7
    )
    res = completion.choices[0].message.content
    res = re.sub(r"\[.*?\]", "", res)
    return res.strip()
