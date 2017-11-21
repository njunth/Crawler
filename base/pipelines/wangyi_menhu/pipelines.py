# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# from scrapy.conf import settings
from base.configs.wangyi_menhu.settings import MONGODB_SERVER, MONGODB_PORT, MONGODB_DBNAME, MONGODB_COLLECTION
from scrapy.exceptions import DropItem


class WangyiScrapyPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            MONGODB_SERVER,
            MONGODB_PORT
        )
        db = connection[MONGODB_DBNAME]
        self.collection = db[MONGODB_COLLECTION]


    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            try:
                self.collection.insert(dict(item))
            except Exception as e:
                print "URL: Item inset error"
            # self.collection.insert(dict(item))
            # log.msg("added to MongoDB database!",level=log.DEBUG, spider=spider)
        return item
