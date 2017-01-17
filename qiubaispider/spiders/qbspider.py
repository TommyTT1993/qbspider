# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.spiders import BaseSpider
from bs4 import BeautifulSoup
from qiubaispider.items import QiubaispiderItem
import re

class QdSpider(BaseSpider):
    name = "QB"
    _cur_index = 1000
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Referer": "http://www.qiushibaike.com/"
    }

    def start_requests(self):
        url = 'http://www.qiushibaike.com/article/118399071'
        self._cur_index += 1
        yield Request(url, callback=self.parse, headers=self.headers, cookies={"__cur_art_index":self._cur_index})

    def verfy(self, text):
        v = re.findall(r"\"([a-zA-Z0-9]{32})\"", text)[0]
        return v
    def parse(self, response):
        try:
            verfy = None
            if str(response.body).find("setCookie") != -1 and str(response.body).find("verify") != -1:
                verfy = self.verfy(str(response.body))
            if verfy:
                yield Request(response.url, callback=self.parse, headers=self.headers, cookies={"__cur_art_index":self._cur_index, "verify":verfy}, dont_filter=True)
                return
            html = BeautifulSoup(response.body, 'html.parser')
            nexturl = html.find('input', attrs={"id":"articlePreLink"}).attrs
            nextid = nexturl['value'].split('/')[-1]
            for i in range(-20, 20):
                nexturl = "%s%s"%("http://www.qiushibaike.com/article/", int(nextid) + i)
                self._cur_index += 1
                yield Request(nexturl, callback=self.parse, headers=self.headers, cookies={"__cur_art_index":self._cur_index}, errback=self.ignore)

            item = QiubaispiderItem()
            thumb = html.find("div", attrs={"class":"thumb"})
            # give up img
            if thumb:
                return
            item['title'] = html.find('div',attrs={"class":"content"}).get_text().strip().strip('\n')
            item['id'] = response.url.split('/')[-1]
            span = html.find('span', attrs={"class":"stats-vote"}).find('i').string
            if str(span).isdigit():
                item['spot'] = int(span)
                yield item
        except Exception as e:
            print(e)
            # eat

    def ignore(self, request):
        pass
