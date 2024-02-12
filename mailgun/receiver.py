from secret import MAIL_SAVE_DIR, DOMAIN_NAME
import json
import os
from archiver import archive


def on_receive(data):
    filename = str(data["timestamp"]) + ".json"

    res = {"from": str(data["sender"]).lower()}

    raw_rec = str(data["recipient"])
    if "," in raw_rec: # 筛查诈骗人的邮箱地址
        for rec in raw_rec.split(","):
            if rec.endswith(DOMAIN_NAME):
                res["bait_email"] = rec
                break
    else:
        res["bait_email"] = raw_rec

    res["title"] = data["Subject"]
    res["content"] = data["stripped-text"]
    if "stripped-signature" in data:
        res["content"] += "\n" + data["stripped-signature"]

    if not os.path.exists(MAIL_SAVE_DIR):
        os.makedirs(MAIL_SAVE_DIR)

    with open(f"{MAIL_SAVE_DIR}/{filename}", "w", encoding="utf8") as f:
        json.dump(res, f) #将python对象res转换为json文件f

    archive(True, res["from"], res["bait_email"], res["title"], res["content"])
