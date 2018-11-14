#_*_encoding:utf-8_*_
"""
@Python -V: 3.X 
@SoftWave: Pycharm
@OS: Win10
@Author: SKYNE
@Contact: 520@skyne.cn
@Time: 2017.11.22
"""

import requests

from lxml import html

class tmtpost(object):

    def __init__(self):
        self.url = 'http://www.tmtpost.com'
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.8", "Cache-Control": "max-age=0",
            "Connection": "keep-alive", "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36", }
        self.session = requests.session()

    def parser(self, url):
        """
        :param url: 需要解析页面的url地址 
        :return: selector 
        """
        response = self.session.get(url=url, headers=self.headers, verify=True)
        if response.status_code == 200:
            selector = html.fromstring(response.text)
            return selector
        else:
            print("request error, please check! @SKYNE")

    def get_url(self):
        """
                :param
                :return: url_list  返回从首页中banner中的文章的url 
                """
        selector = self.parser(self.url)
        url_tmp = list(set(selector.xpath('/html/body//section/div[1]/div//div[3]/a/@href')))
        """
        :param: url {'/article/220006.html', '/article/219989.html', '/article/220008.html'}
        添加self.url，获取完整的url地址。
        """
        url_list = []
        for url in url_tmp:
            url = self.url + url
            url_list.append(url)

        return url_list

    def get_news(self,url):
        """
        :param
        url : 需要进行获取信息的url地址
        flag : 标志位，判断是否抓取成功
        news : 字典，存储各信息
        :return: news 正常返回news，错误返回 -1
        """
        news = {}
        flag = None
        try:
            news['url'] = url
            news['link'] = url[0:7:1] + "m" + url[10:-1:1] + url[-1]
            # print(news['link'])
            selector = self.parser(url)
            news['author'] = u'钛媒体'
            title = selector.xpath ('/html/head/title/text()')[0]

            tmp = ""
            for i in title:
                if i == '-' or i == '|':
                    break
                tmp += i
            # selector.xpath('/html/body/div[5]//div[1]/div[1]/a/span/text()')[0]
            news['title'] = tmp
            content = selector.xpath ('//div[@class="inner"]//p')

            article = ""
            temp = []
            for i in content:
                url = i.xpath ('img/@src')
                temp.append (i.text)
                temp.append (url)

            temp.pop ()

            for i in temp:
                if i:
                    if type (i) == list:
                        article = article + "\n" + "![](" + i[0] + ")" + "\n\n"
                    else:
                        article = article + i + "\n\n"

            summary = ""
            for i in temp:
                if len(summary) > 400:
                    break
                else:
                    if i:
                        if type(i) == list:
                            pass
                        else:
                            summary = summary + i + "\n"

            news[ 'content' ] = summary

            news['text'] = article
            news['cover'] = selector.xpath('//img[@class="aligncenter"]/@src')[0]
            news['labels'] = selector.xpath('/html/body//section//span[1]/a/text()')[0]
            news['service'] = 'Article.AddArticle'
        except Exception as e:
            print("Appear error url=", url, e)
            flag = 1
        if flag == None:
            return news
        else:
            return None
