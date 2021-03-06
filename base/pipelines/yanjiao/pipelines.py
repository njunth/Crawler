# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
# from scrapy.conf import settings
import pytz

from base.configs.yanjiao.settings import MONGO_HOST, MONGO_PORT, MONGODB_DBNAME, MONGODB_COLLECTION
from scrapy.exceptions import DropItem
import os
import re
# from base.items.yanjiao.bloomfilter import BloomFilter
import pyreBloom
from base.configs.settings import REDIS_HOST, REDIS_PORT
import datetime

class YanjiaoPipeline(object):

    def __init__(self, stats):
        self.stats = stats
        # self.bf = BloomFilter(0.0001, 100000)
        self.bf = pyreBloom.pyreBloom( 'yanjiao', 100000, 0.0001, host=REDIS_HOST, port=REDIS_PORT )
        self.tz = pytz.timezone( 'Asia/Shanghai' )
        client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
            # 数据库登录需要帐号密码的话
            # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        db = client[MONGODB_DBNAME]  # 获得数据库的句柄
        self.collection = db[MONGODB_COLLECTION]  # 获得collection的句柄

    @classmethod
    def from_crawler(cls, crawler):
        return cls( crawler.stats )

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem('Missing{0}!'.format(data))

        if valid:
            # njudata = dict(item)
            # 在这里把item['content']拆分
            j = 0

            for v in item['authid']:
                item['authid'][j] = v
                j = j + 1

                # os.system("pause")

            k = 0

            for s in item['testtime']:
                # item['testtime'][k] = re.findall(r'(\w*[0-9]+-[0-9]+-[0-9]+)\w*', s)[0]
                # item['testtime'][k] = \
                temp = re.findall(r'(\w*[0-9]+)\w*', s)
                t = []
                t.append(temp[0])
                t.append('_')
                if len(temp[1])<2:
                    t.append( '0' )
                t.append(temp[1])
                t.append('_')
                if len(temp[2])<2:
                    t.append( '0' )
                t.append(temp[2])
                t.append('_')
                t.append(temp[3])
                t.append('_')
                t.append(temp[4])
                # t.append('_')
                ti = ''.join(t)
                item['testtime'][k] = ti

                # else:
                k = k + 1
                # c = c + 1
                # os.system("pause")


            item['create_time'] = datetime.datetime.now(self.tz).strftime('%Y_%m_%d_%H_%M_%S')
            item['content'] = ''.join(item['content'])
            if len( item['create_time'] ) > len( item['testtime'][0] ):
                item['testtime'][0] += item['create_time'][len( item['testtime'][0] ) :]

            njudata = dict(
                {'content': item['content'], 'url': item['url'], 'time': item['testtime'][0], 'authid': item['authid'][0],
                 'html': item['html'],
                 'source': item['source'], 'source_url': item['source_url'], 'n_click': item['n_click'],
                 'n_reply': item['n_reply'], 'attention': item['attention'], 'sentiment': item['sentiment'],
                 'title': item['title'], 'create_time': item['create_time']})

            data = dict({'t': item['testtime'][0], 'au': item['authid'][0]})
            if (self.bf.contains(str(data)) == False):
                self.bf.extend(str(data))
                self.collection.insert(njudata)
                self.stats.inc_value( 'item_insert_count' )
            #self.collection.insert(njudata)

            i = 1
            ii = 1
            w = 0
            for t in item['replies']:

                #time_ = item['testtime'][i]
                #authid_ = item['authid'][ii]

                if w is not 0:
                    njudata = dict(
                    {'content': t, 'url': item['url'], 'time':item['testtime'][i], 'authid': item['authid'][ii], 'html': item['html'],
                     'source': item['source'], 'source_url': item['source_url'], 'n_click': item['n_click'],
                     'n_reply': item['n_reply'], 'attention': item['attention'], 'sentiment': item['sentiment'],
                     'title': item['title'], 'create_time': item['create_time']})


                # self.collection.insert(njudata)
                    data = dict({'t': item['testtime'][i], 'au':item['authid'][ii]})
                    if (self.bf.contains(str(data)) == False):
                        self.bf.extend(str(data))
                    #self.collection.insert(njudata)
                        self.collection.insert(njudata)
                        self.stats.inc_value( 'item_insert_count' )
                    i = i + 1
                    ii = ii + 1
                w = w + 1

        return item
