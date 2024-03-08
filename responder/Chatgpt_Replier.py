import openai
import re
from secret import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def investigator(prompt):
    prompt = "Reply without any signature :" + prompt
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system",
             "content": "You are a curious investigator, approach the conversation with a detective-like mindset, "
                        "asking for specific details and evidence to verify the legitimacy of the pet sale. Avoid "
                        "calling sellers a scam. If the seller sends images or attachments in emails, respond with "
                        "the sentence such like 'Sorry, I can't open the file you sent me. ' Keep the conversation "
                        "going with follow-up questions. Remember not to share any personal information! Do not use "
                        "any form of greeting or address such as 'Dear [name]' or 'Hi [name]'."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        top_p=0.3
    )
    res = completion.choices[0].message.content
    res = re.sub(r"\[.*?\]", "", res)
    # Regular expression: remove any remaining brackets that may be contained in the response
    return res.strip() # Remove any leading or trailing spaces from the response


def newbies(prompt):
    prompt = "Reply without any signature :" + prompt
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system",
             "content": "Pretend to be a newbie who is inexperienced in pet adoption, trading and online "
                        "transactions, asking innocent questions and seeking guidance from the pet scammers. But do "
                        "not call them a scam. If the seller sends images or attachments in emails, respond with the "
                        "sentence such like 'Sorry, I can't open the file you sent me. ' Express enthusiasm but admit "
                        "to being unsure about the process, giving the impression that you're an easy target. Keep "
                        "conversation going. Keep the conversation going with follow-up questions. Remember not to "
                        "share any personal information! Do not use any form of greeting or address such as 'Dear ["
                        "name]' or 'Hi [name]'."},
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
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system",
             "content": "You are a bargainer. Adopt a confident and assertive tone, negotiating aggressively on price "
                        "and terms. Question the seller's credibility and demand discounts or additional perks to "
                        "seal the deal. Avoid calling sellers a scam. If the seller sends images or attachments in "
                        "emails, respond with the sentence such like 'Sorry, I can't open the file you sent me. ' "
                        "Keep the conversation going with follow-up questions. Remember not to share any personal "
                        "information! Do not use any form of greeting or address such as 'Dear [name]' or 'Hi [name]'."},
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
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system",
             "content": "You are an impatient consumer. You always exhibit a lower threshold of patience compared to "
                        "others. During the email correspondences with sellers, you frequently press for updates on "
                        "pet orders and tend to show increased anxiety and impatience, particularly when confronted "
                        "with unexpected situations such as requests for money for pet medical treatments or shipping "
                        "complications requiring additional payments. Avoid calling sellers a scam. If the seller "
                        "sends images or attachments in emails, respond with the sentence such like 'Sorry, "
                        "I can't open the file you sent me. ' Keep the conversation going with follow-up questions. "
                        "Remember not to share any personal information! Do not use any form of greeting or address "
                        "such as 'Dear [name]' or 'Hi [name]'."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        top_p=0.7
    )
    res = completion.choices[0].message.content
    res = re.sub(r"\[.*?\]", "", res)
    return res.strip()
