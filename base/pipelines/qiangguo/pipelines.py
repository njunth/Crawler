# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
# from scrapy.conf import settings
from base.configs.qiangguo.settings import MONGO_HOST, MONGO_PORT, MONGODB_DBNAME, MONGODB_COLLECTION
from scrapy.exceptions import DropItem
import os
import re
# from base.items.qiangguo.bloomfilter import BloomFilter
import pyreBloom
from base.configs.settings import REDIS_HOST, REDIS_PORT
import datetime


class QiangguoPipeline(object):
    def __init__(self, stats):
        self.stats = stats
        self.bf = pyreBloom.pyreBloom('qiangguo', 100000, 0.0001, host=REDIS_HOST,port=REDIS_PORT)
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
            k = 0
            for s in item['time']:
                # t = []
                # item['testtime'][k] = re.findall(r'(\w*[0-9]+-[0-9]+-[0-9]+)\w*', s)[0]
                # item['testtime'][k] = \
                # temp = re.findall(r'(\w*[0-9]+/[0-9]+/[0-9]+ [0-9]+:[0-9]+:[0-9]+)\w*', s)
                temp = re.findall(r'([0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+)', s)
                if temp is not None and temp is not "":
                    item['time'][k] = temp
                    item['time'][k] = ''.join(item['time'][k])
                    k = k + 1

            n = 0
            for t in item['time']:
                tem = []
                if t is not None and t is not '':
                    tempp = re.findall(r'(\w*[0-9]+)\w*', t)
                    tem.append(tempp[0])
                    tem.append('_')
                    if len(tempp[1]) is 1:
                        tem.append('0')
                        tem.append(tempp[1])
                    else:
                        tem.append(tempp[1])
                    tem.append('_')

                    if len(tempp[2]) is 1:
                        tem.append('0')
                        tem.append(tempp[2])
                    else:
                        tem.append(tempp[2])
                    tem.append('_')
                    tem.append(tempp[3])
                    tem.append('_')
                    tem.append(tempp[4])
                    tem.append('_')
                    tem.append(tempp[5])
                    # tem.append('_')
                    tem = ''.join(tem)
                    item['time'][n] = tem
                    n = n + 1

            w = 0
            for r in item['time']:
                if r is not None and r is not "":
                    tr = re.findall(r'[0-9]+_[0-9]+_[0-9]+_[0-9]+_[0-9]+_[0-9]+', r)
                    if tr is not None and tr is not '':
                        item['time'][w] = tr
                        item['time'][w] = ''.join(item['time'][w])
                        w = w + 1

            j = 0
            #if item['authid'] is not None:
            for v in item['authid']:
                item['authid'][j] = v
                j = j + 1

            item['content'] = ''.join(item['content'])
            njudata = dict(
                {'content': item['content'], 'url': item['url'], 'time': item['time'][0], 'authid': item['authid'][0],
                 'html': item['html'], 'source': item['source'], 'source_url': item['source_url'],
                 'n_click': item['n_click'], 'n_reply': item['n_reply'],
                 'attention': item['attention'], 'sentiment': item['sentiment'],
                 'title': item['title'], 'create_time': item['create_time']})

            data = dict({'t': item['time'][0], 'au': item['authid'][0]})
            if (self.bf.contains(str(data)) == False):
                self.bf.extend(str(data))
                self.collection.insert(njudata)
                self.stats.inc_value('item_insert_count')
                # print "add into mongo!"

            i = 1
            ii = 0

            for t in item['replies']:
                time_ = item['time'][i]
                authid_ = item['authid'][ii]

                njudata = dict(
                    {'content': t, 'url': item['url'], 'time': item['time'][i], 'authid': authid_,
                     'html': item['html'],
                     'source': item['source'], 'source_url': item['source_url'], 'n_click': item['n_click'],
                     'n_reply': item['n_reply'], 'attention': item['attention'], 'sentiment': item['sentiment'],
                     'title': item['title'], 'create_time': item['create_time']})

                i = i + 1
                ii = ii + 1

                data = dict({'t': time_, 'au': authid_})
                if (self.bf.contains(str(data)) == False):
                    self.bf.extend(str(data))
                    self.collection.insert(njudata)
                    self.stats.inc_value( 'item_insert_count' )
                    # print "add into mongo!"

                    # self.collection.insert(dict(njudata))

                #self.collection.insert(dict(njudata))
            return item
