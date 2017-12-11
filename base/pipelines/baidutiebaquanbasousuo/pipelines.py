# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
# from scrapy.conf import settings
from base.configs.baidutiebaquanbasousuo.settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DBNAME, MONGODB_COLLECTION
from base.items.baidutiebaquanbasousuo.bloomfliter import BloomFilter
import os
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')


class MongoDBPipeline(object):
    # def process_item(self, item, spider):
    #     return item
    def __init__(self):
        self.bf=BloomFilter(0.0001,100000)
        port = MONGODB_PORT
        host = MONGODB_HOST
        db_name = MONGODB_DBNAME
        client = pymongo.MongoClient(host=host, port=port)
        db = client[db_name]
        self.post = db[MONGODB_COLLECTION]

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
        for t2 in item['content']:
            t = t2.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
            time_=item['time'][i]
            authid_=item['authid'][ii]
            njudata=dict({'create_time':item['create_time'],'source':item['source'],'source_url':item['source_url'],'url':item['url'],'html':item['html'],'n_click':item['n_click'],'n_reply':item['n_reply'],'content':str(t),'title':item['title'],'attention':item['attention'],'time':time_,'authid':authid_,'sentiment':item['sentiment']})
            if(self.bf.is_element_exist(str(njudata))==False):
                self.bf.insert_element( str( item['time'][i] ) + str( item['authid'][i] ) )
                self.post.insert(njudata)
            i = i + 1
            ii = ii + 1
            print "insert",
            print i
        # njudata = dict(item)
        # self.post.insert(njudata)
        return item
