# coding: utf-8
import os

import requests
import traceback
import random
import re
import time
import json
from collections import deque
from SnuidGenerator import getSnuid

# 忽略SSL证书验证
requests.packages.urllib3.disable_warnings()

# 请求头随机
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"
]

Headers = {
    "Host": "weixin.sogou.com",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://weixin.sogou.com/weixin",
}


# 请求发送时必须得带上
def get_snuid(ua, proxy):
    first_urls = [
        "https://weixin.sogou.com/weixin?type=2&query=%E7%8E%8B%E6%BA%90",
        "https://weixin.sogou.com/weixin?type=2&query=%E6%9C%B1%E4%B8%80%E9%BE%99",
        "https://weixin.sogou.com/weixin?type=2&query=%E7%8E%8B%E4%B8%80%E5%8D%9A",
        "https://weixin.sogou.com/weixin?type=2&query=%E8%82%96%E6%88%98",
        "https://weixin.sogou.com/weixin?type=2&query=%E8%B5%B5%E4%B8%BD%E9%A2%96"
    ]
    headers = {'User-Agent': ua}
    url = random.choice(first_urls)
    rst = requests.get(url=url, proxies=proxy, headers=headers)
    pattern = r'SNUID=(.*?);'
    # snuid为发送请求时必带参数
    snuid = re.findall(pattern, str(rst.headers))
    return snuid[0]


def updateWrite(data):
    files = 'proxiess.txt'
    # 读取数据
    if os.path.exists(files):
        try:
            file = open(files, 'r')
            oldData = file.read().splitlines()
        except IOError as e:
            print(e)
            return 0
        finally:
            file.close()
        # 历史数据 {list:str}
        count = 0
        for x in range(len(data)):
            if isinstance(data[x], str):
                tmp_str = data[x]
            else:
                tmp_str = str(data[x])
            # 增量添加新数据
            if tmp_str not in oldData:
                count += 1
                oldData.append(tmp_str)
            # 写入文件
        print("【增量更新】新增数据：" + str(count) + "条")
        try:
            file = open(files, 'w')
            for x in range(len(oldData)):
                file.write(oldData[x] + '\n')
        except IOError as e:
            print(e)
        finally:
            file.close()


def get_proxy():
    for i in range(20):
        print
        "get proxy try time:", i + 1
        proxy_url = requests.get(
            "http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=3014512010ec47b89407e89d894c7377&count=10&expiryDate=0&format=2&newLine=1"
        ).text

        proxies_list = proxy_url.split(' ')
        updateWrite(proxies_list)
        time.sleep(6)



        #if proxy_url.find('code') > 0:
        #    time.sleep(6)
        #    continue
def getSingleProxy():
    files = 'proxiess.txt'
    try:
        file = open(files, 'r')
        proxiesList = file.read()
        proxiesList = proxiesList.splitlines()
        return {"http": proxiesList[random.randint(0, len(proxiesList)-1)]}
    finally:
        file.close()


def getValidProxy():
    url = 'http://dps.kdlapi.com/api/getdps?orderid=977803630269087&num=1'
    url = requests.get(url)
    return {"http": url.text}


# 获取临时链接
def get_real_url(url, proxy):
    try:
        snuid = get_snuid(random.choice(user_agents), proxy)
        #snuid = getSnuid()
        print('currentSnuid:'+snuid)
        if snuid != None and len(snuid) > 0:
            time.sleep(2)
            Headers['User-Agent'] = random.choice(user_agents)
            Headers['Cookie'] = "SNUID={}".format(snuid[0])
            requests.packages.urllib3.disable_warnings()
            res = requests.get(url + "&k=1&h=f", headers=Headers, proxies=proxy, timeout=5, verify=False)
            url_text = re.findall("\'(\S+?)\';", res.text, re.S)
            base_url = ''.join(url_text)
            i = base_url.find("http://mp.weixin.qq.com")
            if i > 0:
                res.close()
                article_url = base_url[i:len(base_url)]
                print
                article_url
                return article_url
            else:
                return None
        else:
            print
            'get snuid is none'
            return None
    except Exception as e:
        #proxiesList = []
        #try:
        #    print('ProxyNotAv: '+proxy.get("http"))
        #    file = open('proxiess.txt', 'r')
        #    proxiesList = file.read()
        #    proxiesList = proxiesList.splitlines()
        #    proxiesList.remove(proxy.get("http"))
        #finally:
        #    file.close()
        #try:
        #    file = open('proxiess.txt', 'w')
        #    for x in range(0, len(proxiesList)):
        #        file.write(proxiesList[x]+'\n')
        #finally:
        #   file.close()
        return get_real_url(url, getValidProxy())




# 烦人的单双引号
def baoli(cc):
    sc = cc.replace("'", "\\\'").replace('"', '\\\"')
    return sc





if __name__ == '__main__':
    #url = "https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgSwcDAwBgpcSuptmBLQllctAczgHBxbRh8lqXa8Fplpd9oNWD11wNJgBaBzSmLtpNQ4e4rjx_e0KdWGJwtXRgRxyKzCKg2itt3f8c5VsKCfwCRc-siBFP_RrbgAWHo0RtCtS7Dw4PE9toh8FeuPPJznB9XsSQfAMs-3eSPmA_YCMN0UZB-OcOcXXmeq4_z9FmG0ERDqplnY0GqcIk5tZn7cXS-e4Yz84xMA..&type=2&query=%E5%90%8C%E4%BB%81%E5%A0%82&token=empty&k=1&h=f"
    #url  = "https://mp.weixin.qq.com/s?src=11&timestamp=1578030908&ver=2073&signature=zmE*-lQsMmbfmzcg20CtauZ3obs0E3BrYzgxeYjFBLctFK8zz7GXVOMMRFxEhdoIoQ3sqWAsVcqRfTfPOWe6ARW9e4LPJVjLzm1uKQ-3kKfpeAgwLcMArrYn6qGaEyS7&new=1"
    #arurl = get_real_url(url)
    proxy = {"http": "36.56.145.2:39725"}
    prosfsdf = getSingleProxy()
    res = requests.get("https://www.baidu.com/", proxies=prosfsdf,  timeout=3)
    print(getValidProxy())
    #print(arurl)
    #proxy  = get_proxy()
    #print(proxy)

