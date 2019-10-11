#! -*- coding:utf-8 -*-
'''
获取SNUID的值
'''
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



