#coding:utf-8
#python3
import time

import requests
import random
from bs4 import BeautifulSoup
import json

from urllib import parse
import SnuidGenerator
from GetWeChatUrl import  get_real_url
from GetWeChatUrl import getSingleProxy
from GetWeChatUrl import get_snuid
from GetWeChatUrl import getValidProxy
"""
全局变量区域
"""
user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" ,
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/71.0.3578.98Safari/537.36"
    ]

global proxies


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

def set_proxies_list():
    data = open("proxies.json","r").read()
    global proxies
    proxies = json.loads(data)
    # 打印代理的信息
    return proxies

def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies


def get_Referer():
    referer= 'https://weixin.sogou.com/weixin?type=2&query=%E5%90%8C%E4%BB%81%E5%A0%82&ie=utf8&s_from=input&_sug_=n&_sug_type_=1&w=01015002&oq=&ri=0&sourceid=sugg&sut=0&sst0=1570865981022&lkt=0%2C0%2C0&p=40040108'
    return referer

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

# 用于获取网页的基本内容
def get_content(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/77.0.3865.90 Safari/537.36",
            "Referer": get_Referer()
        }

        cookies = {
            "CXID" : "1DB214E49FB5A670216D942812AE4EF5",
            "ad":"uyllllllll2NN1QFlllllVCTSBGlllllTHal9Zllll9llllljOxlw@@@@@@@@@@@",
            #搜狗服务器分配的ID，短时间内不变，作用域Session
            "SUID":"65FD73CA3108990A000000005E044186",
            "SUV":"1577337223009084",
            "SMYUV":"1569480527228598",
            "UM_distinctid":"16d6c544d7f4d-0258fb17966ea6-67e1b3f-1fa400-16d6c544d813ac",
            "ABTEST":"5|1570673115|v1",
            #防反爬重点，每个SNUID达到使用次数限制后，需更新才能继续访问，不然跳转到验证码页面
            "SNUID": SnuidGenerator.getSnuid(),
            #"SNUID": get_snuid(random.choice(user_agents), getValidProxy()),
            "IPLOC":"CN5101",
            "JSESSIONID":"aaalw50R4h-H-bQWvfD8w",
            "successCount":"1|Thu, 26 Dec 2019 06:48:53 GMT"
        }
        r = requests.get(url, headers=headers,proxies = getValidProxy(),  cookies=cookies)
        # print(r.text)
        # return r.text.encode(r.encoding).decode("utf-8")
        return r.text
    except Exception as e:
        print(e)
        exit(1)

# 存储文件的内容
def store_file(file_name, content):
    open(file_name, "wb").write(str(content).encode())
    #print("Save file succesfully!")

class WeiXinSpider():
    def __init__(self):
        # 爬取的搜索入口点
        self.weixin_search_url = "https://weixin.sogou.com/"
        # 热点消息
        self.hot_topic_list = []



    def hot_word_search_analysis(self, homepageContent):
        hpSoup = BeautifulSoup(homepageContent, "html.parser")
        # 定位目标的标签
        hot_news = hpSoup.find_all("ol")[0]
        # 解析标签，获取标题，url
        hot_news_list = hot_news.find_all("li")
        for topic in hot_news_list:
            # 存储的字典的格式
            topic_dic = {
                "id": None,
                "rank": None,
                "url": None
            }
            topic_dic["id"] = topic.a.get("title")
            topic_dic["url"] = topic.a.get("href")
            topic_dic["rank"] = topic.i.get_text()
            self.hot_topic_list.append(topic_dic)
        print(self.hot_topic_list)

    # 返回存储的列表
    def get_hot_topic_list(self):
        if len(self.hot_topic_list) == 0:
            self.hot_word_search_analysis(get_content(self.weixin_search_url))
        return self.hot_topic_list


    def main(self):
        # result = get_content(self.weixin_search_url)
        # store_file("saerch.html", result)
        content = open("saerch.html","rb").read()
        self.hot_word_search_analysis(content.decode())
        store_file("url_list.txt", str(self.get_hot_topic_list()))

class WeiXinSearch():
    def __init__(self):
        # http://weixin.sogou.com/weixin?type=2&ie=utf8&s_from=hotnews&query=%E7%81%B0%E7%86%8A%E4%BA%A4%E6%98%93%E9%97%B9%E4%B9%8C%E9%BE%99'
        # 搜索的网址
        self.__search_url = ""
        # 搜索页面的url
        self.__search_page = None
        # 所有页面组成的列表
        self.page_url_list = []
        # 所有文章的url列表
        self.article_url_list = []
        set_proxies_list()

    # 传入需要收索的中文内容
    def set_search_content(self, search_word):
        url_code = parse.quote(search_word)
        self.__search_url = "http://weixin.sogou.com/weixin?type=2&query={}".format(url_code)


    #传入需要搜索的网址
    def set_search_url(self, url):
        self.__search_url = url

    # 获取初始的搜索界面
    def __get_search_page_content(self):
        if self.__search_url=="":
            print("Please set search url")
            exit(0)
        self.__search_page = get_content(self.__search_url)
        return self.__search_page

    def __get_page_list(self):
        search_page_soup = BeautifulSoup(self.__search_page, "html.parser")
        store_file("同仁堂.html", self.__search_page)
        all_div = search_page_soup.find_all("div")
        page_list_div = None
        # 定位页面列表的位置
        for divc in all_div:
            if (divc["class"][0]=="p-fy") and (divc["id"]=="pagebar_container"):
                # if divc["class"][0] == "news-box":all_div
                page_list_div = divc
            # 基本的页面结构
        url_base = "https://weixin.sogou.com/weixin"

        # 获取 a 标签下面的内容
        page_list_a = page_list_div.find_all("a")[:-1]
        # 存储到相应的列表中
        self.page_url_list.append(self.__search_url)
        for i in page_list_a:
            url = url_base + i.get("href")
            self.page_url_list.append(url)
        # print(self.page_url_list)

    def get_article_list(self):
        if len(self.page_url_list) == 0:
            print("Please get page url list!")
            exit(0)
        print("page_len"+str(len(self.page_url_list)))
        for url in self.page_url_list:
            url_list = self.__search_page_article(url)
            try:
                tmpfile = open('pageurlList.txt', 'a+')
                for i in range(0, len(url_list)):
                    tmpfile.write(url_list[i]+'\n')
            finally:
                tmpfile.close()
            self.article_url_list.extend(url_list)
        return self.article_url_list



    def __search_page_article(self, url):
        page_content = get_content(url)
        soup = BeautifulSoup(page_content, "html.parser")
        all_div = soup.find_all("ul")
        # 锁定 article 的全部标签的位置
        article_div = None
        for divi in all_div:
            if divi["class"][0] == "news-list":
                article_div = divi
        if article_div == None:
            print("Wrong!")
            exit(0)
        # 定位所有的 a 标签
        h3_all_div = article_div.find_all("h3")
        url_list = []
        content_list = []
        for i in h3_all_div:
            url = i.a.get("href")
            url_list.append('https://weixin.sogou.com'+url)
            #url_list.append(get_real_url('https://weixin.sogou.com' + url, getValidProxy()))
        if len(url_list)==0:
            print("Wrong")
            exit(0)
        return url_list

    def get_page_content(self, url):
        page_content = get_content(url)
        soup = BeautifulSoup(page_content, "html.parser")
        all_div = soup.find_all("ul")
        # 锁定 article 的全部标签的位置
        article_div = None
        for divi in all_div:
            if divi["class"][0] == "news-list":
                article_div = divi
        if article_div == None:
            print("Wrong!")
            exit(0)
        p_all_div = article_div.find_all("p")
        content_list = []
        for i in p_all_div:
            content_list.append(i.text)
        if len(content_list) == 0:
            print("Wrong")
            exit(0)
        return content_list

    def get_page_url_list(self):
        return self.page_url_list

    # 传入搜索的首地址，自动完成文章的全部url获取
    def module_auto(self, search_url):
        self.set_search_url(search_url)
        self.__get_search_page_content()
        self.__get_page_list()
        self.list = self.get_article_list()
        self.self_list = self.list
        li = self.self_list
        #li = self.page_url_list
        return li
        # fileObject = open('url_3.txt','w')
        # for i in li:
        #     fileObject.write(i)
        #     fileObject.write('\n')
        # print(li)

    def main(self):
       # search_url = "http://weixin.sogou.com/weixin?type=2&ie=utf8&s_from=hotnews&query=%E5%90%8C%E4%BB%81%E5%A0%82%E8%87%B4%E6%AD%89"
        search_url='http://weixin.sogou.com/weixin?type=2&ie=utf8&s_from=hotnews&query=%E5%88%98%E5%BC%BA%E4%B8%9C%E8%87%B4%E6%AD%89'
        file_name = '同仁堂致歉.html'
        # self.set_search_url(search_url)
        # self.__get_search_page_content()
        # store_file(file_name, self.__search_page)
        # self.__search_page = open(file_name, "rb").read()
        # self.__search_page_article(search_url)
        self.module_auto(search_url)

class WeiXinArticle():
    def __init__(self, article_url_list):
        self.article_url_list = article_url_list

    def __get_article_dic(self, url):
        content = get_content(url)

    def main(self):
        # url
        url ="http://mp.weixin.qq.com/s?src=11&timestamp=1545213031&ver=1283&signature=pssN*ZDFHAbAg9zKUY1*d6Gk662edASh3VVMQsKDPTigLLopkjEHeRXs*Aq5IB8aKTxFc8H5I7LR20WneLDPSG5fjESqRW50Z224DI06TikKo1WGdI8prc2oLbTTVT-q&new=1"
        self.__get_article_dic(url)
#WeiXinSearch().main()