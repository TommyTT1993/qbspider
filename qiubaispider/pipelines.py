# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.exceptions import DropItem
import qiubaispider
import re

class QiubaispiderPipeline(object):
    def __init__(self):
        url = 'mongodb://{user}:{password}@{host}:{port}/{dbname}'.format(
            user=qiubaispider.MONGOUSER,
            password=qiubaispider.MONGOPASS,
            host="127.0.0.1",
            port=27017,
            dbname="admin"
        )
        self.mongo = MongoClient(url, connect=False)
        super(QiubaispiderPipeline, self).__init__()

    def process_item(self, item, spider):
        db = self.mongo.get_database("spider")
        collection = db.get_collection("qiubai")
        collection.insert_one({"_id":item['id'], "title":item['title'], "spot":item['spot']})
        return item


class FilterPipeline(object):

    def __init__(self):
        super(FilterPipeline, self).__init__()
        self.filter_word = u"糗事百科|糗百|糗友|割|匿了|必须匿|糗事"
        self.reg = re.compile(self.filter_word)

    def process_item(self, item, spider):
        title = item['title']
        if not self.reg.search(title):
            return item
        else:
            pass