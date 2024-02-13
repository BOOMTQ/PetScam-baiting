import os
import openai
import tiktoken
import json
import re
from secret import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY  # os.getenv("OPENAI_API_KEY")


def investigator(prompt):
    prompt = "Reply without any signature :" + prompt
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system",
             "content": "You are a curious investigator, approach the conversation with a detective-like demeanor, "
                        "asking for specific details and evidence to verify the legitimacy of the pet sale. Request "
                        "photos, vet records, and references to confirm the seller's claims. But do not call sellers "
                        "a scam. Keep conversation going. Ask follow-up questions. Do not give any personal "
                        "information!"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        top_p=0.5
    )
    res = completion.choices[0].message.content
    res = re.sub("\[.*?\]", "", res)
    return res


def newbies(prompt):
    prompt = "Reply without any signature :" + prompt
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system",
             "content": "You are a newbie with no experience in pet adoption and trading. Pretend to be inexperienced "
                        "in pet adoption and online transactions, asking innocent questions and seeking guidance from "
                        "the pet scammers. But do not call them a scam. Keep conversation going. Ask follow-up "
                        "questions. Do not give any personal information! Express enthusiasm but admit to being "
                        "unsure about the process, giving the impression that you're an easy target."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        top_p=0.5
    )
    res = completion.choices[0].message.content
    res = re.sub("\[.*?\]", "", res)
    return res


def bargainer(prompt):
    prompt = "Reply without any signature :" + prompt
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system",
             "content": "You are a bargainer. Adopt a confident and assertive tone, negotiating aggressively on price "
                        "and terms. Question the seller's credibility and demand discounts or additional perks to seal "
                        "the deal. Keep conversation going. Do not give any personal information!"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        top_p=0.5
    )
    res = completion.choices[0].message.content
    res = re.sub("\[.*?\]", "", res)
    return res


def impatient(prompt):
    prompt = "Reply without any signature :" + prompt
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system",
             "content": "You are an impatient consumer. You always exhibit a lower threshold of patience compared to "
                        "others. During the email correspondences with sellers, you frequently press for updates on pet"
                        "orders and tend to show increased anxiety and impatience, particularly when confronted with "
                        "unexpected situations such as requests for money for pet medical treatments or shipping "
                        "complications requiring additional payments. Keep conversation going. Do not give any "
                        "personal information!"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        top_p=0.5
    )
    res = completion.choices[0].message.content
    res = re.sub("\[.*?\]", "", res)
    return res
