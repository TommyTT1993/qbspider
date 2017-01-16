# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import qiubaispider

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
