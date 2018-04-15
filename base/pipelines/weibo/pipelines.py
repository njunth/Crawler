# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import pytz
import pymongo
import time
from base.configs.weibo.settings import MONGO_HOST,MONGO_PORT,MONGODB_COLLECTION,MONGODB_DBNAME
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class WeiboPipeline(object):
    def __init__(self, stats):
        self.stats = stats
        client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        db = client[MONGODB_DBNAME]
        self.collection = db[MONGODB_COLLECTION]
        self.tz = pytz.timezone( 'Asia/Shanghai' )
        #self.collection.remove({})

    @classmethod
    def from_crawler(cls, crawler):
        return cls( crawler.stats )

    def process_item(self, item, spider):
        #print item
        id = item['_id']
        res = self.collection.find_one({'_id':id})
        #print res
        keyword = ''
        createstr = ''
        timestr = ''
        if res != None:
            # print "update"
            keywords = res['keyword']
            createstr = res['create_time']
            timestr = res['time']
            keyset = set(keywords.split('_'))
            if item['keyword'] not in keyset:
                keyword = keywords + '_' + item['keyword']
            else:
                keyword = keywords
        #keyword = (unicode(keyword) + unicode(item['keyword']) + '_').encode('UTF-8')
        else:
            # print "new data"
            keyword = item['keyword']
            createstr  = datetime.datetime.now(self.tz)
            timestr = item['time']
        #print keyword
        self.collection.save({
            '_id': item['_id'],
            'content': item['content'],
            'source': "新浪微博",
            'n_forward': item['n_forward'],
            'n_comment': item['n_comment'],
            'n_like': item['n_like'],
            'attention': '0',
            'sentiment': '0',
            #'keyword': item['keyword'],
            'keyword' : keyword,
            'time': timestr,
            'url': item['url'],
            'authid': item['authid'],
            'create_time': createstr.strftime('%Y_%m_%d_%H_%M_%S')
        })
        self.stats.inc_value( 'item_insert_count' )
        return item