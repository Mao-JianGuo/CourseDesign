#coding:utf-8
#python3

import WeiXinSpider as WXS
from bs4 import BeautifulSoup
import requests
import random
import re
import threading
import datetime
import logging
import json
import urllib3

logging.basicConfig(filename='log.log',
                    format='%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p',
                    level=logging.DEBUG)

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

"""
代理的网址
    list={'1': 'http://www.xicidaili.com/nt/', # xicidaili国内普通代理
          '2': 'http://www.xicidaili.com/nn/', # xicidaili国内高匿代理
          '3': 'http://www.xicidaili.com/wn/', # xicidaili国内https代理
          '4': 'http://www.xicidaili.com/wt/'} # xicidaili国外http代理
"""

proxies = []
pagenum = []

class IpProxy():
    def __init__(self):
        self.proxy_url = "http://www.xicidaili.com/nn/"
        logging.info("开始获取代理IP，访问的地址：{}".format(self.proxy_url))
        self.headers = {
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # "Accept-Encoding": "gzip,deflate,br",
            # "Accept-Language": "zh-CN,zh;q=0.9",
            # "Cache-Control": "max-age=0",
            # "Connection": "keep-alive",
            # "Host": "www.xicidaili.com",
            "User-Agent": random.choice(user_agent_list)
        }
        self.__random_number = random.randint(1, 200)

    def thread(self):
        url = self.__get_random_url()
        ip_list = self.__get_ip_list(url)
        self.__valid_proxy(ip_list)

    # 随机获取一页的IP地址
    def __get_random_url(self):
        num = 1
        while(1):
            num = self.__random_number
            if num not in pagenum:
                pagenum.append(num)
                break
        url = self.proxy_url + str(num)
        logging.info("获取第{}页的信息：{}".format(url.split("/")[-1],url))
        return url

    # 获取指定页面的数据
    def __get_ip_list(self, url):
        r = requests.get(url, headers=self.headers)
        web_soup = BeautifulSoup(r.text, "html.parser")
        logging.info("="*20)
        # 开始解析页面
        ip_div_all = web_soup.find_all("tr")
        ip_list = []
        # 获取爬取页面的 ip 和 port
        for i in range(1,len(ip_div_all)):
            # 暂存字典
            temp_dic = {
                "ip":None,
                "port":None,
                "type":None
            }
            info = ip_div_all[i]
            info_2 = info.find_all("td")
            # print(info_2)
            # 需要去掉的字符
            sub_patter = r"<.*?>"
            temp_dic["ip"] = re.sub(sub_patter,"",str(info_2[1]))
            temp_dic["port"] = re.sub(sub_patter,"",str(info_2[2]))
            temp_dic["type"] = str.lower(re.sub(sub_patter,"", info_2[5].text))
            # print("ip: {}, port: {}".format(ip, port))
            ip_list.append(temp_dic)

        # 打印获取的字典
        # for i in ip_list:
        #     print("ip: {}, port: {}".format(i.get("ip"), i.get("port")))

        return ip_list

    """
    temp_dic = {
        "ip":None,
        "port":None
    }
    """
    def __valid_proxy(self, ip_list):
        logging.info("筛选能够使用的IP地址")

        # print("对{}个IP信息，进行筛选.......".format(len(ip_list)))
        logging.info("对{}个IP信息，进行筛选.......".format(len(ip_list)))

        test_url = "http://weixin.sogou.com/weixin?type=2&ie=utf8&s_from=hotnews&query=%E5%90%8C%E4%BB%81%E5%A0%82"
        # test_url = "https://www.baidu.com"
        valid_proxies = []
        for i in ip_list:
            # ip = i.get("type")+"://"+i.get("ip")+":"+ i.get("port")
            ip = "http://" + i.get("ip") + ":" + i.get("port")
            # 处理成为代理IP的格式
            proxies_t = {"http":ip}
            print(proxies_t)
            try:
                response = requests.get(test_url, proxies=proxies_t, headers=self.headers, timeout=3)
                self.__sougou_test_proxy(response.text)
            except TimeoutError as timeError:
                logging.info("ip : {} 不可用".format(proxies_t.get("http")))
                continue
            except urllib3.exceptions.MaxRetryError as tiemout:
                logging.info("ip : {} 不可用".format(proxies_t.get("http")))
                continue
            except requests.exceptions.ConnectTimeout as conout:
                logging.info("ip : {} 不可用".format(proxies_t.get("http")))
                continue
            except KeyError as ke:
                logging.info("ip : {} 不可用".format(proxies_t.get("http")))
                continue
            except Exception as e:
                logging.error(e)
                logging.info("ip : {} 不可用".format(proxies_t.get("http")))
                continue
            logging.info("ip : {} 可用".format(proxies_t.get("http")))
            valid_proxies.append(proxies_t)
        proxies.extend(valid_proxies)

    # 针对搜狗微信搜索界面的代理测试
    def __sougou_test_proxy(self, html):
        search_page_soup = BeautifulSoup(html, "html.parser")
        all_div = search_page_soup.find_all("div")
        page_list_div = None
        # 定位页面列表的位置
        for divc in all_div:
            # print(divc.attrs)
            if (divc["class"][0]=="p-fy") and (divc["id"]=="pagebar_container"):
                # if divc["class"][0] == "news-box":
                page_list_div = divc

# 整个模块的入口的位置
def auto_main():
    logging.info("多线程开始爬取")
    start_time = datetime.datetime.now()
    # 设置爬取多少个网页
    threads = []
    # 每个线程爬取一个xici的页面
    for i in range(8):
        logging.info("线程{}，创建！".format(i+1))
        t = threading.Thread(target=IpProxy().thread)
        threads.append(t)
    for thread in threads:
        thread.start()
    for i in threads:
        i.join()
    end_time =datetime.datetime.now()
    logging.info("代理池爬取完毕")
    logging.info("Ip数量:{}，用时：{}".format(len(proxies), end_time-start_time))

    data = json.dumps(proxies)
    WXS.store_file("proxiess.txt", data)
    return proxies

def another_test():
    proxies_t = {"http": "http://27.155.84.233:8081"}
    headers = {
        "User-Agent": random.choice(user_agent_list)
    }
    test_url = "http://weixin.sogou.com/weixin?type=2&ie=utf8&s_from=hotnews&query=%E5%90%8C%E4%BB%81%E5%A0%82"
    response = requests.get(test_url, proxies=proxies_t, headers=headers, timeout=3)
    print(response.text)

# 将日志的信息清零
def log_clear():
    open("log.log","wb")

if __name__ == "__main__":
    # log_clear()
    # another_test()
    auto_main()