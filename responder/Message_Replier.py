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
             "content": "You seems like a curious investigator, leave one or two sentences of message to show that you are interested in this website and what to get your own pet."},
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
             "content": "You seems like a newbie who is inexperienced in pet adoption, trading and online transactions. Leave one or two sentences of message to show that you are interested in this website and what to get your own pet. "},
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
             "content": "You seems like a bargainer, leave one or two sentences of message to show that you are interested in this website and what to get your own pet."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        top_p=0.5
    )
    res = completion.choices[0].message.content
    res = re.sub("\[.*?\]", "", res)
    return res


def impatient_consumer(prompt):
    prompt = "Reply without any signature :" + prompt
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system",
             "content": "You seems like a impatient consumer, leave one or two sentences of message to show that you are interested in this website and what to get your own pet."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        top_p=0.5
    )
    res = completion.choices[0].message.content
    res = re.sub("\[.*?\]", "", res)
    return res
