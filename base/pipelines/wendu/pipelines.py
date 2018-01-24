# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from pymongo import MongoClient
# from scrapy.conf import settings
from base.configs.wendu.settings import MONGO_HOST,MONGO_PORT,MONGO_DB,MONGO_COLL

class WenduPipeline(object):
    def __init__(self, stats):
        self.stats = stats
        self.client = MongoClient(MONGO_HOST, MONGO_PORT)
        mdb = self.client[MONGO_DB]
        self.collection = mdb[MONGO_COLL]

    @classmethod
    def from_crawler(cls, crawler):
        return cls( crawler.stats )
    
    def process_item(self, item, spider):
        data = dict(item)
        self.collection.insert(data)
        self.stats.inc_value( 'item_insert_count' )
        return item
    
    def close_spider(self, spider):
        self.client.close()