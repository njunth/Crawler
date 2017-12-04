# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
# from scrapy.conf import settings
from base.configs.zhonggong.settings import MONGO_HOST,MONGO_PORT,MONGO_DB,MONGO_COLL

class ZhonggongPipeline(object):
    def __init__(self):
        self.client = MongoClient(MONGO_HOST, MONGO_PORT)
        mdb = self.client[MONGO_DB]
        self.collection = mdb[MONGO_COLL]
    
    
    def process_item(self, item, spider):
        data = dict(item)
        self.collection.insert(data)
        return item
    
    def close_spider(self, spider):
        self.client.close()
