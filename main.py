#a main file

from pafd import *
from login import *
import sys
import wechat
from dorm_electricity import *

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
    geo = daily_fudan.geo_info
    last_info = daily_fudan.last_info
    daily_fudan.close(1)

    dorm_electricity = Elec(uid=uid, psw=psw, url_login='https://uis.fudan.edu.cn/authserver/login',
             url_code="https://zlapp.fudan.edu.cn/fudanelec/wap/default/info")
    dorm_electricity.login()
    remaining_electricity = dorm_electricity.get_dorm_electricity()
    dorm_electricity.close(1)

    p = wechat.push(title='每日打卡与宿舍电量汇报', message='今日打卡成功，宿舍剩余电量：'+ remaining_electricity + '\n打卡位置：' + geo)
    sys.exit(p)
