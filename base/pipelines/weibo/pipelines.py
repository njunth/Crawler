# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from weibo.settings import MONGO_HOST,MONGO_PORT,MONGODB_COLLECTION,MONGODB_DBNAME
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class WeiboPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        db = client[MONGODB_DBNAME]
        self.collection = db[MONGODB_COLLECTION]

    def process_item(self, item, spider):
        #print item
        id = item['_id']
        res = self.collection.find_one({'_id':id})
        #print res
        keyword = ''
        if res != None:
            keywords = res['keyword']
            keyset = set(keywords.split('_'))
            if item['keyword'] not in keyset:
                keyword = keywords + '_' + item['keyword']
            else:
                keyword = keywords
        #keyword = (unicode(keyword) + unicode(item['keyword']) + '_').encode('UTF-8')
        else:
            keyword = item['keyword']
        #print keyword
        self.collection.save({
            '_id': item['_id'],
            'content': item['content'],
            'source': 'sina_weibo',
            'n_forword': item['n_forword'],
            'n_comment': item['n_comment'],
            'n_like': item['n_like'],
            'attention': '0',
            'sentiment': '0',
            #'keyword': item['keyword'],
            'keyword' : keyword,
            'time': item['time'],
            'url': item['url'],
            'publisher': item['publisher']
        })
        return item
