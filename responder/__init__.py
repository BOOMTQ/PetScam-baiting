import json
import os
from collections import namedtuple

from secret import MODEL_HISTORY_PATH
from responder.replier import Replier, ChatReplier1, ChatReplier2, ChatReplier3, ChatReplier4

replier_list = [ChatReplier1(), ChatReplier2(), ChatReplier3(), ChatReplier4()]

ReplyResult = namedtuple("ReplyResult", ["name", "text"])

if not os.path.exists(os.path.dirname(MODEL_HISTORY_PATH)):
    os.makedirs(os.path.dirname(MODEL_HISTORY_PATH))

if not os.path.exists(MODEL_HISTORY_PATH):
    d = {}
    for r in replier_list:
        d[r.name] = 0
    with open(MODEL_HISTORY_PATH, "w", encoding="utf8") as f:
        json.dump(d, f)


def get_replier_by_name(name):  # 根据名称返回回复者实例。
    for r in replier_list:
        if r.name == name:
            return r
    return None


def update_replier_history(scam_email, sol_name):  # 更新回复者的选择计数。
    try:
        with open(MODEL_HISTORY_PATH, "r", encoding="utf8") as f:
            history_data = json.load(f)

        # if it is the first conversation with this "scam_email"
        if scam_email not in history_data['scam_emails']:
            history_data['scam_emails'][scam_email] = {"has_replied": True, "sol_used": sol_name}
            history_data['sol_counts'][sol_name] = history_data['sol_counts'].get(sol_name, 0) + 1
        else:
            history_data['sol_counts'][sol_name] = history_data['sol_counts'].get(sol_name, 0)

        with open(MODEL_HISTORY_PATH, "w", encoding="utf8") as f:
            json.dump(history_data, f, indent=4)
    except Exception as e:
        print(f"An error occurred while updating history for {sol_name}: {e}")
