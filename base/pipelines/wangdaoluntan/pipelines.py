# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
# from scrapy.conf import settings
from base.configs.wangdaoluntan.settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DBNAME, MONGODB_COLLECTION
from base.items.wangdaoluntan.bloomfliter import BloomFilter
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
        for v in item['authid']:
            vv = v.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
            item['authid'][j]= vv
            j=j+1
            #os.system("pause")

        k=0
        for s in item['time']:
            s2=s.replace('-','_').replace(' ','_').replace(':','_')
            time_str= re.findall(r'\w*_([0-9]+_[0-9]+_[0-9]+_[0-9]+_[0-9]+)\w*',s2)[0]
            timelist=time_str.split('_')
            kk=0
            for t in timelist:
                if (len(t)==0):
                    timelist[kk]='00_'
                elif(len(t)==1):
                    timelist[kk]='0'+t+'_'
                else:
                    timelist[kk]=t+'_'
                kk=kk+1
            final_str=list(''.join(timelist))
            final_str.pop()
            item['time'][k]=''.join(final_str)
            item['time'][k]=item['time'][k]+'_00'
            k=k+1
        i=0
        ii=0
        if(len(item['content'])==len(item['authid'])):
            for tt in item['content']:
                t = tt.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
                time_=item['time'][i]
                authid_=item['authid'][ii]
                print i
                njudata=dict({'create_time':item['create_time'],'source':item['source'],'source_url':item['source_url'],'url':item['url'],'html':item['html'],'n_click':item['n_click'],'n_reply':item['n_reply'],'content':str(t),'title':item['title'],'attention':item['attention'],'time':time_,'authid':authid_,'sentiment':item['sentiment']})
                if(self.bf.is_element_exist(str(item['time'][i])+str(item['authid'][i]))==False):
                    self.bf.insert_element(str(item['time'][i])+str(item['authid'][i]))
                    self.post.insert(njudata)
                i = i + 1
                ii = ii + 1

        # njudata = dict(item)
        # self.post.insert(njudata)
        return item
