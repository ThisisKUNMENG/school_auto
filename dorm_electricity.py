#a script to get dorm remaining electricity

import requests
import json
#from bs4 import BeautifulSoup
import login

class Elec(login.Fudan):
    def get_dorm_electricity(self):
        get_info = self.session.get(
            'https://zlapp.fudan.edu.cn/fudanelec/wap/default/info')
        if get_info.status_code == 200:
            try:
                info = json.loads(get_info.text)
                remain_elec = str(info['d']['fj_surplus'])
            except Exception as e:
                remain_elec = "failed to get dorm electricity with exception" + str(e)
        else:
            remain_elec = 'failed to get drom electricity with status code' + str(get_info.status_code)
        return remain_elec

uid, psw = login.get_account()

