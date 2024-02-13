import requests
import time

from secret import MAIL_SAVE_DIR

# 指定的URL
url = 'http://127.0.0.1:10234/income'

# 构造表单数据
data = {
    "timestamp": str(int(time.time())),  # 当前时间戳，转换为字符串
    "sender": "gegavog488@fahih.com",
    "recipient": "io96961@liveonline.ninja",
    "Subject": "More About Your Future Puppy!",
    "stripped-text": "Dear Rodney,\nWe've successfully received your deposit. Congratulations, Coco is now reserved just for you! We're starting the preparations for their journey to your home.\nWe'll keep you updated every step of the way. The remaining balance will be due before the delivery date, which we will confirm shortly.\nCheers,\nPure Teacup Maltese"
    # 可以添加 0"stripped-signature": "邮件签名", 如果需要
}

# 发送POST请求，使用data参数而非json，以发送表单数据
response = requests.post(url, data=data)

# 检查响应
if response.status_code == 200:
    print("Successfully delivered")
else:
    print("Failed delivered, response code:", response.status_code)

print("Emails will be saved to:", MAIL_SAVE_DIR)
