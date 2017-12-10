# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# from scrapy.conf import settings
from base.configs.sina.settings import MONGO_HOST, MONGO_PORT, MONGODB_DBNAME, MONGODB_COLLECTION
from scrapy.exceptions import DropItem
import os
import re
from base.items.sina.bloomfilter import BloomFilter
import datetime

class SinaPipeline(object):

    def __init__(self):

        self.bf = BloomFilter(0.0001, 100000)
        client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
            # 数据库登录需要帐号密码的话
            # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        db = client[MONGODB_DBNAME]  # 获得数据库的句柄
        self.collection = db[MONGODB_COLLECTION]  # 获得collection的句柄

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem('Missing{0}!'.format(data))

        if valid:
            #njudata = dict(item)
            #在这里把item['content']拆分
            j = 0

            for v in item['authid']:
                item['authid'][j] = v
                j = j + 1

                # os.system("pause")

            k = 0

            for s in item['testtime']:
                #item['testtime'][k] = re.findall(r'(\w*[0-9]+-[0-9]+-[0-9]+)\w*', s)[0]
                #item['testtime'][k] = \
                temp = re.findall(r'(\w*[0-9]+)\w*', s)
                t = []
                t.append(temp[0])
                t.append('_')
                t.append(temp[1])
                t.append('_')
                t.append(temp[2])
                t.append('_')
                t.append(temp[3])
                t.append('_')
                t.append(temp[4])
                #t.append('_')
                ti = ''.join(t)
                item['testtime'][k] = ti

                #else:
                k = k + 1
                #c = c + 1
                # os.system("pause")

            item['create_time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            i = 0
            ii = 0
            for t in item['replies']:
               
                time_ = item['testtime'][i]
                authid_ = item['authid'][ii]
                i = i + 1
                ii = ii + 1
                #if t is "  ":
                njudata = dict({'content':t,'url':item['url'],'time':time_,'authid':authid_,'html':item['html'],'source':item['source'],'source_url':item['source_url'],'n_click':item['n_click'],'n_reply':item['n_reply'],'attention':item['attention'],'sentiment':item['sentiment'],'title':item['title'],'create_time':item['create_time']})
                #self.collection.insert(njudata)
                data = dict({'t':time_,'au':authid_})
                if (self.bf.is_element_exist(str(data)) == False):
                    self.bf.insert_element(str(data))
                    self.collection.insert(njudata)
            #self.collection.insert(dict(item))

        return item