import requests

import bs4
from bs4 import BeautifulSoup
import re


class PageParsing:

    def __init__(self,html_doc):
        self.page_dict = {
            "title":None,    # 标题
            "public_address":None,  # 公众号
            "content": ''  # 内容
        }
        Soup = BeautifulSoup(html_doc, 'lxml')
        if(len(Soup.findAll('div', id='page-content'))  < 1):
            self.flag = 0
            return
        page_content: BeautifulSoup = Soup.findAll('div', id='page-content')[0]


        content = ''
        self.flag = 1

        self.page_dict['title'] = str(Soup.title.text.strip())
        self.page_dict['public_address']= str(page_content.a.text.strip())
        # for k in page_content.descendants:
        #     print(k)

        # for k in page_content.findAll('p'):
        #     for l in k.descendants:
        #         if(type(l) == bs4.element.NavigableString):
        #             print(l)

        for i in page_content.findAll('p'):
            if('class' in i.attrs   and len(i['class'])!=0 and i['class'][0] == 'profile_meta'):
                continue
            elif(i.a!=None and 'href' in i.a.attrs):
                continue


            for j in i.descendants:


                if(type(j) != bs4.element.NavigableString):
                    if('style' not in j.attrs):
                        continue
                if(type(j) == bs4.element.NavigableString):
                    if('图片来源' in j):
                        continue
                    #页面解析
                   # print("1"+str(j))
                    # if(j.parent.name =='script'):
                    #     self.flag = 0
                    if('转账' in str(j)):
                        break
                    if('个人公众号' in str(j)):
                        break
                    if('文 |'  in str(j)):
                        continue
                    if('来源 |' in str(j)):
                        continue
                    if('点击上方' in str(j)):
                        continue
                    if('首发 |' in str(j)):
                        continue
                    if('点击上面' in str(j)):
                        continue
                    if('replace' in  str(j)):
                        ste = re.sub("[A-Za-z0-9\!\%\[\]\,\。]", "", str(j))
                        a = ste.find('\"')
                        b=ste.find('\"', a+1)
                        print(ste[a+1:b])
                        content =content + str(ste[a+1:b]).strip()
                        continue
                    #print(str(j).strip())
                    content =content + str(j).strip()
        if(str(content) == '已发送'):
            flag = 0
        self.page_dict['content'] = content

    def  get_dict(self):
          return self.page_dict

# r = requests.get('https://mp.weixin.qq.com/s?src=11&timestamp=1545726493&ver=1317&signature=pPnmKDiHP0SnYn7A3LMwR8BzPddRcbgu8bbW0GqqmEhVEWPRExeMLNq4ltaHGu4iin5drKgJnQImjiN4dvbsf0524KssgCZ8XkKmg6nRtCfBo2zrG59oXLAo1gPzurU*&new=1')
#
#

# html_doc = open('1.html',encoding='utf-8')
# p = PageParsing(html_doc)
# #
# print(p.get_dict())



