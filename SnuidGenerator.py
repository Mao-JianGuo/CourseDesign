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
        headers = {
            # "User-Agent": random.choice(user_agent_list)
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        }
        cookies = {
            "CXID": "9A9BB967E5EE5412594BC70A108AB335",
            "ad": "jV9rvyllll2NoH52lllllVLA1D1lllll1AOuvkllll9lllllRylll5@@@@@@@@@@@",
            # 搜狗服务器分配的ID，短时间内不变，作用域Session
            "SUID": "4A6629D23108990A000000005DA2D391",
            "SUV": "1570952081661135",
            "SMYUV": "1569480527228598",
            #"UM_distinctid": "16d6c544d7f4d-0258fb17966ea6-67e1b3f-1fa400-16d6c544d813ac",
            # 防反爬重点，每个SNUID达到使用次数限制后，需更新才能继续访问，不然跳转到验证码页面
            "SNUID": getSnuid(),
            "IPLOC": "CN5101",
            "sct":"2",
            "ld":"1kllllllll2NoHnNlllllVLA1DYlllll1AOuvkllllwlllllRylll5@@@@@@@@@@",
            "LSTMV":"512%2C85",
            "LCLKINT": "2584",
            "ABTEST":"2|1570952139|v1",
            "PHPSESSID":"2nnnaei7mhef1tg94jsv7cc7b2",
            "seccodeRight":"success;",
            "successCount":"1|Sun, 13 Oct 2019 07:41:09 GMT",
            "JSESSIONID":"aaapDWqSz1d4befSLir1w"
        }
        r = requests.get(url, headers=headers, cookies=cookies)
        wxid = json.loads(r.content.decode('utf-8'))
        return wxid.get('openid')
    except Exception as e:
        print('[Error]:API:getWechatIdByChineseWord')
        exit(1)

if __name__ =='__main__':
    print(getWechatIdByChineseWord('为自己健康代言'))
