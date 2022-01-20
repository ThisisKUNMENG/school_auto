#a script to send message to wechat

import requests

pushkey_SCU = "SCU176210T38ce782eeb7c584032783542e6eec4ac60b5e0b254ad9"
pushkey_SCT = "SCT59286TuS2ZzTEZPOTv1JIE97Yp2Ylj"
pushurl_SCU = f"https://sc.ftqq.com/{pushkey_SCU}.send"
pushurl_SCT = f"https://sctapi.ftqq.com/{pushkey_SCT}.send"

def push_old(title, message):
    response = requests.post(pushurl_SCU, {"text": title, "desp": message})
    if response.status_code == 200:
        print(f"发送通知状态：{response.content.decode('utf-8')}")
        return True
    else:
        print(f"发送通知失败：{response.status_code}")
        return False

def push(title, message):
    response = requests.post(pushurl_SCT, {"text": title, "desp": message, "channel": 9})
    if response.status_code == 200:
        print(f"发送通知状态：{response.content.decode('utf-8')}")
        return True
    else:
        print(f"发送通知失败：{response.status_code}")
        return False

