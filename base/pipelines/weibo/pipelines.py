# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# import time
import datetime
from base.configs.weibo.settings import MONGO_HOST,MONGO_PORT,MONGODB_COLLECTION,MONGODB_DBNAME
import sys
import pytz
reload(sys)
sys.setdefaultencoding('utf-8')

class WeiboPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        db = client[MONGODB_DBNAME]
        self.collection = db[MONGODB_COLLECTION]
        self.tz = pytz.timezone('Asia/Shanghai')
        #self.collection.remove({})

    def process_item(self, item, spider):
        #print item
        id = item['_id']
        res = self.collection.find_one({'_id':id})
        #print res
        keyword = ''
        createstr = ''
        if res != None:
            keywords = res['keyword']
            createstr = res['create_time']
            keyset = set(keywords.split('_'))
            if item['keyword'] not in keyset:
                keyword = keywords + '_' + item['keyword']
            else:
                keyword = keywords
        #keyword = (unicode(keyword) + unicode(item['keyword']) + '_').encode('UTF-8')
        else:
            keyword = item['keyword']
            d = datetime.datetime.now(self.tz)
            createstr = d.strftime('%Y_%m_%d_%H_%M_%S')
            print createstr
            # createstr = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
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
            'time': item['time'],
            'url': item['url'],
            'authid': item['authid'],
            'create_time': createstr
        })
        return item