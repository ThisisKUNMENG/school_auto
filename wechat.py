#a script to send message to wechat

import requests
import os

pushkey_SCU = os.getenv("pushkey_SCU")
pushkey_SCT = os.getenv("pushkey_SCT")
Push = True

if pushkey_SCU == None and pushkey_SCT == None:
    if os.path.exists("pushkey.txt"):
        print("读取账号中……")
        with open("pushkey.txt", "r") as old:
            raw = old.readlines()
        if (raw[0][:3] != "SCU"):
            print("pushkey.txt 内容无效, 请手动修改内容")
        pushkey_SCU = (raw[0].split(":"))[1].strip()
        pushkey_SCT = (raw[1].split(":"))[1].strip()
    else:
        print("未找到pushkey.txt, 判断缺少pushkey")
        Push = False

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

