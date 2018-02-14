# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from base.configs.xinjingbao_menhu.settings import MONGODB_SERVER, MONGODB_PORT, MONGODB_DBNAME, MONGODB_COLLECTION
from scrapy import log

import pymongo
# from scrapy.conf import settings
from scrapy.exceptions import DropItem


class XinjingbaoScrapyPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            MONGODB_SERVER,
            MONGODB_PORT
        )
        db = connection[MONGODB_DBNAME]
        self.collection = db[MONGODB_COLLECTION]
        print self.collection.database

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            #log.msg("added to MongoDB database!", level=log.INFO, spider=spider)
        return item
