# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
# from scrapy.conf import settings
from base.configs.chinakaoyanluntan.settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DBNAME, MONGODB_COLLECTION
# from base.items.chinakaoyanluntan.bloomfliter import BloomFilter
from base.configs.settings import REDIS_HOST, REDIS_PORT
import pyreBloom
import os
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

class MongoDBPipeline(object):
    # def process_item(self, item, spider):
    #     return item
    def __init__(self, stats):
        self.stats = stats
        self.bf=pyreBloom.pyreBloom('chinakaoyanluntan', 100000, 0.0001, host=REDIS_HOST,port=REDIS_PORT)
        port = MONGODB_PORT
        host = MONGODB_HOST
        db_name = MONGODB_DBNAME
        client = pymongo.MongoClient(host=host, port=port)
        db = client[db_name]
        self.post = db[MONGODB_COLLECTION]

    @classmethod
    def from_crawler(cls, crawler):
        return cls( crawler.stats )

    def process_item(self, item, spider):
        j=0
        for v in item['authid']:
            vv = v.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
            item['authid'][j]= vv
            j=j+1
            #os.system("pause")

        k=0
        for s in item['time']:
            s2=s.replace('-','_').replace(' ','_').replace(':','_')
            s3= re.findall(r'\w*_([0-9]+_[0-9]+_[0-9]+_[0-9]+_[0-9]+)\w*',s2)[0]
            item['time'][k]=s3+'_00'
            k=k+1
            #os.system("pause")
        i=0
        ii=0
        for t in item['content']:
            tt2 = t.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
            tt3 = re.split('varbdShare_config=.+' , tt2)
            tt = ''.join(tt3)
            time_=item['time'][i]
            authid_=item['authid'][ii]
            # print i
            njudata=dict({'create_time':item['create_time'],'source':item['source'],'source_url':item['source_url'],'url':item['url'],'html':item['html'],'n_click':item['n_click'],'n_reply':item['n_reply'],'content':str(tt),'title':item['title'],'attention':item['attention'],'time':time_,'authid':authid_,'sentiment':item['sentiment']})
            # print self.bf.is_element_exist(str(item['time'][i])+str(item['authid'][i]))
            if(self.bf.contains(str(item['time'][i])+str(item['authid'][i]))==False):
                self.bf.extend(str(item['time'][i])+str(item['authid'][i]))
                self.post.insert(njudata)
                self.stats.inc_value( 'item_insert_count' )
            i = i + 1
            ii = ii + 1
        # njudata = dict(item)
        # self.post.insert(njudata)
        return item
