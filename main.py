# coding:utf-8
# python3
import time

from DataStorage import DataStorage
from PageParsing import PageParsing
from WeiXinSpider import WeiXinSearch
from urllib.parse import quote
from bs4 import BeautifulSoup
import requests
import random

def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list

def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies

if __name__ == "__main__":
    # WeiXinSearch().main()
    print('【爬虫启动中】初始化参数中......')
    print('【爬虫启动中】参数初始化完成')
    #time.sleep(0.5)
    key = input('请输入搜索词:')
    usip = input('请输入公众号名称：')
    print('【输入完成】关键词：{},  公众号：{}'.format(key,usip));
    #key = "同仁堂"
    #usip = '为自己健康代言'
    # wxid= SnuidGenerator.getWechatIdByChineseWord(usip)
    key_urlEncoded = quote(key, 'utf-8')
    usip_urlEncoded = quote(usip, 'utf-8')
    search_url = "https://weixin.sogou.com/weixin?type=2&s_from=input&query={}&ie=utf8&_sug_=y&_sug_type_=&w=01019900&sut=3284&sst0=1577337391745&lkt=1%2C1577337391643%2C1577337391643".format(key_urlEncoded)
    print('【首页连接解析】连接解析完成 url：{}'.format(search_url))
    page_url_list_tmp = WeiXinSearch().module_auto(search_url)
    page_url_list = []
    print('【连接爬取成功】共{}条页面连接，开始数据爬取'.format(len(page_url_list)))
    #print("url_list:\n"+url_list)

    result = []
    flag = 0

    for i in range(0, len(page_url_list)):
        html_doc = requests.get(page_url_list[i]).text
        p = PageParsing(html_doc)
        print('[' + str(round(((i / len(page_url_list)) * 100))) + '%] ' + '第' + str(i) + '页解析完毕')
        if (p.get_dict()['content'] != '' and p.flag == 1):
            result.append(p.get_dict())
        flag = i

    dataFile = DataStorage(key, usip, 'update')
    dataFile.writeData(result)
