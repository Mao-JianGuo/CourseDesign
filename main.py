# coding:utf-8
# python3
import time

from DataStorage import DataStorage
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
    WeiXinSearch().initParams()
    print('【爬虫启动中】参数初始化完成')
    time.sleep(0.5)
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
    page_url_list = WeiXinSearch().module_auto(search_url)
    print('【连接爬取成功】共{}条页面连接，开始数据爬取'.format(len(page_url_list)))
    #print("url_list:\n"+url_list)

    result = []
    flag = 0

    for i in range(0, len(page_url_list)):
        page_contents = WeiXinSearch().get_page_content(page_url_list[i])
        count = 0;
        for j in range(0 , len(page_contents)):
            count += len(page_contents[j])
            result.append(page_contents[j])
        info = '['+str(round(((i/len(page_url_list))*100)))+'%] '+'第'+str(i)+'页数据爬取并解析完成  共爬取'+str(len(page_contents))+'条数据，共'+str(count)+'字符'
        print(info)

    dataFile = DataStorage(key, usip, 'cover')
    dataFile.writeData(result)
