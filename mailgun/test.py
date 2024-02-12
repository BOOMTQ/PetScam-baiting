import requests
import time

# 指定的URL
url = 'http://127.0.0.1:10234/income'

# 构造表单数据
data = {
    "timestamp": str(int(time.time())),  # 当前时间戳，转换为字符串
    "sender": "tamopew400@oprevolt.com",
    "recipient": "recipient@example.com",
    "Subject": "Urgent: Unusual Activity Detected On Your Bank Account",
    "stripped-text": "Dear valued customer,\n\nWe have detected some unusual activity on your bank account that suggests a possible unauthorized transaction attempt. For your security, we have temporarily suspended access to your account.\n\nTo verify your identity and restore account access, please confirm your bank card details and social security number. You can do this by replying directly to this email with the required information.\n\nWe understand this may be inconvenient, but your account safety is our top priority. Please act swiftly to prevent any potential financial loss.\n\nThank you for your cooperation and understanding.\n\nSincerely,\nCustomer Service Team",
    # 可以添加 "stripped-signature": "邮件签名", 如果需要
}

# 发送POST请求，使用data参数而非json，以发送表单数据
response = requests.post(url, data=data)

# 检查响应
if response.status_code == 200:
    print("Successfully delivered")
else:
    print("Failed delivered, response code:", response.status_code)
