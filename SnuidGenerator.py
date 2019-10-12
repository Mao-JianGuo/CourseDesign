#! -*- coding:utf-8 -*-
'''
获取SNUID的值
'''
from urllib.parse import quote

import json
import requests
import re

def getSnuid():
    url="https://www.sogou.com/web?query=333&_asf=www.sogou.com&_ast=1488955851&w=01019900&p=40040100&ie=utf8&from=index-nologin"
    headers={
        "Cookie":"ABTEST=5|1570673115|v1;IPLOC=CN5101;SUID=13C0D2DE4C238B0A5D774593000E0288;JSESSIONID=aaajVZjidb_ttcYsqKq1w;SUIR=1488956269"
    }
    f=requests.head(url,headers=headers).headers
    tmp_str = f._store.get('set-cookie')[1]
    snuid = re.search('SNUID=.+?;',tmp_str,0).group()
    return snuid[6:-1]

#通过公众号的中文名称获取wxid，以构造对特定公众号内容检索的查询url
def getWechatIdByChineseWord(name):
    #for test
    name_urlEncode  = quote(name, 'utf-8')
    url='https://weixin.sogou.com/weixin?zhnss=1&type=1&ie=utf8&query={}'.format(name)

    try:
        # url = 'http://www.xicidaili.com/nn/'
        headers = {
            # "User-Agent": random.choice(user_agent_list)
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        }
        cookies = {
            "CXID": "1DB214E49FB5A670216D942812AE4EF5",
            "ad": "uyllllllll2NN1QFlllllVCTSBGlllllTHal9Zllll9llllljOxlw@@@@@@@@@@@",
            # 搜狗服务器分配的ID，短时间内不变，作用域Session
            "SUID": "13C0D2DE4C238B0A5D774593000E0288",
            "SUV": "006B15E6D229600D5D8988FFD3AC4033",
            "SMYUV": "1569480527228598",
            "UM_distinctid": "16d6c544d7f4d-0258fb17966ea6-67e1b3f-1fa400-16d6c544d813ac",
            "ABTEST": "5|1570673115|v1",
            # 防反爬重点，每个SNUID达到使用次数限制后，需更新才能继续访问，不然跳转到验证码页面
            "SNUID": getSnuid(),
            "IPLOC": "CN5101",
            "JSESSIONID": "aaajVZjidb_ttcYsqKq1w",
            "successCount": "2|Thu, 10 Oct 2019 06:52:14 GMT"
        }
        r = requests.get(url, headers=headers, cookies=cookies)
        wxid = json.loads(r.content.decode('utf-8'))
        return wxid
    except Exception as e:
        print(e)
        exit(1)
