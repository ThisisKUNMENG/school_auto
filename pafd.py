#a script to auto-report pafd


import json
import time
import os
from json import loads as json_loads
from os import path as os_path, getenv
from sys import exit as sys_exit
from getpass import getpass
#import get_dorm_elec
import re
import base64
import easyocr
import io
import numpy
from PIL import Image
from PIL import ImageEnhance
import requests
from requests import session, post, adapters
import platform

import login
import wechat

adapters.DEFAULT_RETRIES = 5

class Zlapp(login.Fudan):
    last_info = ''
    geo_info = ''

    def check(self):
        """
        检查
        """
        print("◉检测是否已提交")
        get_info = self.session.get(
            'https://zlapp.fudan.edu.cn/ncov/wap/fudan/get-info')
        last_info = get_info.json()

        print("◉上一次提交日期为:", last_info["d"]["info"]["date"])

        position = last_info["d"]["info"]['geo_api_info']
        position = json_loads(position)
        geo_info = position['formattedAddress']

        print("◉上一次提交地址为:", geo_info)
        # print("◉上一次提交GPS为", position["position"])
        # print(last_info)

        # 改为上海时区
        os.environ['TZ'] = 'Asia/Shanghai'
        if platform.system() != "Windows":
            time.tzset()
        today = time.strftime("%Y%m%d", time.localtime())
        print("◉今日日期为:", today)
        if last_info["d"]["info"]["date"] == today:
            print("\n*******今日已提交*******")
            return False
        else:
            print("\n\n*******未提交*******")
            self.last_info = last_info["d"]["oldInfo"]
            return True

    def read_captcha(self, img_byte):
        img = Image.open(io.BytesIO(img_byte)).convert('L')
        enh_bri = ImageEnhance.Brightness(img)
        new_img = enh_bri.enhance(factor=1.5)

        image = numpy.array(new_img)
        reader = easyocr.Reader(['en'])
        horizontal_list, free_list = reader.detect(image, optimal_num_chars=4)
        character = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        allow_list = list(character)
        allow_list.extend(list(character.lower()))

        result = reader.recognize(image,
                                  allowlist=allow_list,
                                  horizontal_list=horizontal_list[0],
                                  free_list=free_list[0],
                                  detail=0)
        return result[0]

    def validate_code(self):
        img = self.session.get(self.url_code).content
        return self.read_captcha(img)

    def checkin(self):
        """
        提交
        """
        headers = {
            "Host": "zlapp.fudan.edu.cn",
            "Referer": "https://zlapp.fudan.edu.cn/site/ncov/fudanDaily?from=history",
            "DNT": "1",
            "TE": "Trailers",
            "User-Agent": self.UA
        }

        print("\n\n◉◉提交中")

        geo_api_info = json_loads(self.last_info["geo_api_info"])
        province = self.last_info["province"]
        city = self.last_info["city"]
        district = geo_api_info["addressComponent"].get("district", "")

        while (True):
            print("◉正在识别验证码......")
            code = self.validate_code()
            print("◉验证码为:", code)
            self.last_info.update(
                {
                    "tw": "13",
                    "province": province,
                    "city": city,
                    "area": " ".join((province, city, district)),
                    # "sfzx": "1",  # 是否在校
                    # "fxyy": "",  # 返校原因
                    "code": code,

                }
            )
            # print(self.last_info)
            save = self.session.post(
                'https://zlapp.fudan.edu.cn/ncov/wap/fudan/save',
                data=self.last_info,
                headers=headers,
                allow_redirects=False)

            save_msg = json_loads(save.text)["m"]
            print(save_msg, '\n\n')
            time.sleep(0.1)
            if (json_loads(save.text)["e"] != 1):
                break

if __name__ == '__main__':
    uid, psw = get_account()

    # print(uid, psw)
    zlapp_login = 'https://uis.fudan.edu.cn/authserver/login?' \
                  'service=https://zlapp.fudan.edu.cn/site/ncov/fudanDaily'
    code_url = "https://zlapp.fudan.edu.cn/backend/default/code"
    daily_fudan = Zlapp(uid, psw,
                        url_login=zlapp_login, url_code=code_url)
    daily_fudan.login()

    daily_fudan.check()
    daily_fudan.checkin()
    # 再检查一遍
    daily_fudan.check()

    daily_fudan.close(1)
