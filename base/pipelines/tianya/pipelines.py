# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# from scrapy.conf import settings
from base.configs.tianya.settings import MONGO_HOST, MONGO_PORT, MONGODB_DBNAME, MONGODB_COLLECTION
from scrapy.exceptions import DropItem

import json
class Tianyav2Pipeline(object):
    def __init__(self):
            # 链接数据库
        client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
            # 数据库登录需要帐号密码的话
            # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        db = client[MONGODB_DBNAME]  # 获得数据库的句柄
        self.collection = db[MONGODB_COLLECTION]  # 获得collection的句柄

    def process_item(self, item, spider):
            # self.coll.insert(dict(item))
        valid = True
        for data in item:
            #print data
            if not data:
                valid = False
                raise DropItem('Missing{0}!'.format(data))

        if valid:
            self.collection.insert(dict(item))
                # log.msg('question added to mongodb database!',
                #       level=log.DEBUG, spider=spider)
            #return item
        return item
