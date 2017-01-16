from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from qiubaispider.items import QiubaispiderItem

class QdSpider(BaseSpider):
    name = "QB"
    start_urls = [
        "http://www.qiushibaike.com/article/118393179",
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//title/text()').extract()
        spot = hxs.select("//span[@class='stats-vote']/i[1]/text()").extract()
        item = QiubaispiderItem()
        if spot and title and len(title) > 0 and len(spot) > 0:
            item['title'] = title[0].strip().strip('\n')
            item['id'] = response.url.split('/')[-1]
            item['spot'] = spot[0]
        return item



