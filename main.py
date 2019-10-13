# coding:utf-8
# python3
from DataStorage import DataStorage
from WeiXinSpider import WeiXinSearch
from PageParsing import PageParsing
from urllib.parse import quote
from bs4 import BeautifulSoup
import requests
import random
import SnuidGenerator

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

    # key = input('请输入搜索词:')
    key = "同仁堂"
    usip = '为自己健康代言'
    wxid= SnuidGenerator.getWechatIdByChineseWord(usip)
    key_urlEncoded = quote(key, 'utf-8')
    usip_urlEncoded = quote(usip, 'utf-8')
    search_url = "http://weixin.sogou.com/weixin?type=2&ie=utf8&s_from=hotnews&query={}&tsn=0&ft=&et=&interation=&wxid={}&usip={}".format(key_urlEncoded, wxid, usip_urlEncoded)
    print(search_url)
    url_list = WeiXinSearch().module_auto(search_url)
    #print("url_list:\n"+url_list)

    result = []
    flag = 0

    for i in range(0, len(url_list)):
        html_doc = requests.get(url_list[i]).text
        p = PageParsing(html_doc)
        print('['+str(round(((i/len(url_list))*100)))+'%] '+'第'+str(i)+'页解析完毕')
        if(p.get_dict()['content'] != '' and p.flag == 1 ):
            result.append(p.get_dict())
        flag = i

    dataFile = DataStorage(key, usip, 'update')
    dataFile.writeData(result)
