# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from base.configs.baidusousuo.settings import MONGODB_DBNAME,MONGODB_COLLECTION,MONGODB_HOST,MONGODB_PORT

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ScrapyBaiduPipeline(object):
    def __init__(self, stats):
        self.stats = stats
        client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[MONGODB_DBNAME]
        self.collection = db[MONGODB_COLLECTION]

    @classmethod
    def from_crawler(cls, crawler):
        return cls( crawler.stats )

    def process_item(self, item, spider):
        self.collection.save({
            'url':item['url'],
            'title':item['title'],
            'content':item['abstract'],
            'keyword':item['keyword'],
            'time':item['time'],
            'create_time':item['time'],
            'source':'百度搜索',
            'html':''
        })
        self.stats.inc_value( 'item_insert_count' )
        return item
