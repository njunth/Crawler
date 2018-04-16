#encoding=utf-8

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
# from scrapy.conf import settings
import redis
import time

from base.configs.baidutiebaquanbasousuo.settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DBNAME, MONGODB_COLLECTION
from base.items.baidutiebaquanbasousuo.bloomfliter import BloomFilter
# from base.items.Bloomfilter import BloomFilter
import os
import sys
import re
import pyreBloom
from base.configs.settings import REDIS_HOST, REDIS_PORT
reload(sys)
sys.setdefaultencoding('utf-8')


class MongoDBPipeline(object):
    # def process_item(self, item, spider):
    #     return item
    def __init__(self, stats):
        self.r = redis.StrictRedis( host=REDIS_HOST, port=REDIS_PORT )
        if self.r.exists("baidutiebaquanbasousuo.0"):
            print "baidutiebaquanbasousuo.0 exist"
            self.bf = pyreBloom.pyreBloom( 'baidutiebaquanbasousuo', 100000, 0.0001, host=REDIS_HOST, port=REDIS_PORT )
            print self.r.ttl( 'baidutiebaquanbasousuo.0' )
        else:
            print "creat baidutiebaquanbasousuo.0"
            self.bf = pyreBloom.pyreBloom( "baidutiebaquanbasousuo", 100000, 0.0001, host=REDIS_HOST, port=REDIS_PORT )
            tests = "Hello baidutiebaquanbasousuo!"
            self.bf.extend( tests )
            print self.r.expire( 'baidutiebaquanbasousuo.0', 60*60*24*7 )
            time.sleep(3)

            print self.r.ttl( 'baidutiebaquanbasousuo.0' )
        # self.bf = pyreBloom.pyreBloom( 'baidutiebaquanbasousuo', 100000, 0.0001, host=REDIS_HOST, port=REDIS_PORT )
        port = MONGODB_PORT
        host = MONGODB_HOST
        db_name = MONGODB_DBNAME
        client = pymongo.MongoClient(host=host, port=port)
        db = client[db_name]
        self.post = db[MONGODB_COLLECTION]
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls( crawler.stats )

    def process_item(self, item, spider):
        j=0
        for v2 in item['authid']:
            v = v2.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
            item['authid'][j]= v
            j=j+1
            #os.system("pause")
        k=0
        for s in item['time']:
            s2=s.replace('-','_').replace(' ','_').replace(':','_')
            s3=s2+'_00'
            item['time'][k]= s3
            k=k+1
        i=0
        ii=0
        iii=0
        for t2 in item['content']:
            t = t2.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
            time_=item['time'][i]
            authid_=item['authid'][ii]
            # source_=item['source'][iii]
            source_ = u"百度贴吧"
            source_url_=item['url'][iii]
            title_=item['title'][iii]
            if not source_url_.startswith('http'):
                source_url_="http://tieba.baidu.com"+source_url_
            njudata=dict({'create_time':item['create_time'],'source':source_,'source_url':item['source_url'],'url':source_url_,'html':item['html'],'n_click':item['n_click'],'n_reply':item['n_reply'],'content':str(t),'title':title_,'attention':item['attention'],'time':time_,'authid':authid_,'sentiment':item['sentiment']})
            njudata1=time_+authid_+t
            print self.r.ttl( 'baidutiebaquanbasousuo.0' ),
            if self.r.ttl( 'baidutiebaquanbasousuo.0' ) == -1:
                print self.r.exists( 'baidutiebaquanbasousuo.0' ),
                # self.bf = pyreBloom.pyreBloom( "baidutiebaquanbasousuo", 100000, 0.0001, host=REDIS_HOST, port=REDIS_PORT )
                # tests = "Hello baidutieba!"
                # self.bf.extend( tests )
                print self.r.expire( 'baidutiebaquanbasousuo.0', 60*60*24*7 )
            if(self.bf.contains(str(njudata1))==False):
                self.bf.extend( str(njudata1) )
                self.post.insert(njudata)
                self.stats.inc_value( 'item_insert_count' )
            i = i + 1
            ii = ii + 1
            iii = iii+1
            ##print "insert",
            ##print i

        # njudata = dict(item)
        # self.post.insert(njudata)
        return item
