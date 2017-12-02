# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
# from scrapy.conf import settings
from base.configs.chinakaoyan.settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DBNAME, MONGODB_COLLECTION


class MongoDBPipeline(object):
    # def process_item(self, item, spider):
    #     return item
    def __init__(self):
        port = MONGODB_PORT
        host = MONGODB_HOST
        db_name = MONGODB_DBNAME
        client = pymongo.MongoClient(host=host, port=port)
        db = client[db_name]
        self.post = db[MONGODB_COLLECTION]

    def process_item(self, item, spider):
         njudata = dict(item)
         print item['current_url']
         self.post.insert(njudata)
         return item
