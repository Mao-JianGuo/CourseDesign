#! -*- coding:utf-8 -*-
'''
获取SNUID的值
'''
from urllib.parse import quote

import json
import requests
import re
#防反爬取措施方案有两种
#1.使用代理池模拟数量众多的真实用户去爬取数据：ipProxy类实现此功能
#优点：从物理层面绕过防反爬机制
#缺点：免费的代理池不稳定，容易失效，且代理数量有限，存在瓶颈
#2.经过对搜狗搜索引擎的访问机制和防爬机制的研究，我们发现搜狗会对同一ip的访问进行频率限制，并且检测是真实的用户访问还是爬虫
#最重要的鉴别字段是在请求头中设置的Cookie其中的snuid字段，该字段有一定的生成规则，并且在使用达到100次之后会失效，经过对搜狗源码的分析，我们找到了实时更新snuid的方法
#到此，只要访问达到100次之后，调用该接口即可更新snuid，可以实现单一ip无限访问
def getSnuid():
    url="https://www.sogou.com/web?query=333&_asf=www.sogou.com&_ast=1488955851&w=01019900&p=40040100&ie=utf8&from=index-nologin"
    headers={
        "Cookie":"ABTEST=5|1570673115|v1;IPLOC=CN5101;SUID=13C0D2DE4C238B0A5D774593000E0288;JSESSIONID=aaajVZjidb_ttcYsqKq1w;SUIR=1488956269"
    }
    f=requests.head(url, headers=headers).headers
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
    #print(getWechatIdByChineseWord('为自己健康代言'))
    print(getSnuid())
