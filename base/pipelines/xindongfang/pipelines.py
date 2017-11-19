# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class XindongfangPipeline(object):
    def __init__(self):
        self.client = MongoClient(settings['MONGO_HOST'], settings['MONGO_PORT'])
        mdb = self.client[settings['MONGO_DB']]
        self.collection = mdb[settings['MONGO_COLL']]
    
    
    def process_item(self, item, spider):
        data = dict(item)
        self.collection.insert(data)
        return item
    
    def close_spider(self, spider):
        self.client.close()