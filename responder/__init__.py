import json
import os
from collections import namedtuple, defaultdict

from secret import MODEL_HISTORY_PATH
from responder.replier import Replier, TemplateReplier, ChatReplier1, ChatReplier2, ClassifierReplier# NeoEnronReplier, NeoRawReplier

replier_list = [ChatReplier1(), ChatReplier2(), ClassifierReplier()] # [ClassifierReplier(), NeoEnronReplier(), NeoRawReplier()]

ReplyResult = namedtuple("ReplyResult", ["name", "text"])

if not os.path.exists(os.path.dirname(MODEL_HISTORY_PATH)):
    os.makedirs(os.path.dirname(MODEL_HISTORY_PATH))

if not os.path.exists(MODEL_HISTORY_PATH):
    d = {}
    for r in replier_list:
        d[r.name] = 0
    with open(MODEL_HISTORY_PATH, "w", encoding="utf8") as f:
        json.dump(d, f)


def get_replier_by_name(name): #根据名称返回回复者实例。
    for r in replier_list:
        if r.name == name:
            return r
    return None


def get_replier_randomly() -> Replier: #根据之前选择的历史记录随机选择回复者并更新选择计数。
    with open(MODEL_HISTORY_PATH, "r", encoding="utf8") as f:
        j = json.load(f)

    count_dict = defaultdict(int, j)
    res = min(count_dict, key=count_dict.get)
    count_dict[res] += 1
    with open(MODEL_HISTORY_PATH, "w", encoding="utf8") as f:
        json.dump(count_dict, f)

    return get_replier_by_name(res)


def get_reply_random(mail_body) -> ReplyResult: # 从给定的随机选择的回复者中检索回复mail_body
    r = get_replier_randomly()
    text = r.get_reply(mail_body)
    res = ReplyResult(r.name, text)
    return res


# def get_reply_with_solution(mail_body, name) -> str:
#     r = get_replier_by_name(name)
#     if r is not None:
#         return r.get_reply(mail_body)
#     else:
#         return "SOLUTION_NOT_FOUND"

# r = get_replier_by_name("Classifier")
# # add = "piyushbajaj71@gmail.com"
# print(r.get_reply("Hello"))
