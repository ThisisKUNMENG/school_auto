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
            info = json.loads(get_info.text)
            remain_elec = str(info['d']['fj_surplus'])
        else:
            remain_elec = 'failed to get'
        return remain_elec

uid, psw = login.get_account()

