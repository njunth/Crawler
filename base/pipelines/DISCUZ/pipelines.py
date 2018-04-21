# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
# from scrapy.conf import settings
import pyreBloom
from base.configs.DISCUZ.settings import MONGO_HOST, MONGO_PORT, MONGODB_DBNAME, MONGODB_COLLECTION
from scrapy.exceptions import DropItem
# from base.items.DISCUZ.bloomfilter import BloomFilter
import re
from base.configs.settings import REDIS_HOST, REDIS_PORT
import datetime

class DiscuzPipeline(object):
    def __init__(self, stats):
        self.stats = stats
        # self.bf = BloomFilter(0.0001, 100000)
        self.bf = pyreBloom.pyreBloom( 'Discuz', 100000, 0.0001, host=REDIS_HOST, port=REDIS_PORT )
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
            j = 0
            for v in item['authid']:
                item['authid'][j] = v
                j = j + 1

            k = 0
            for s in item['time']:
                # print s
                temp = re.findall(r'(\w*[0-9]+)\w*', s)
                # print temp
                t = []
                t.append(temp[0])
                t.append('_')
                for n in range(1, 6):
                    if n < len(temp):
                        if len(temp[n]) < 2:
                            t.append( '0' )
                            t.append( temp[n] )
                            t.append( '_' )
                        else:
                            t.append(temp[n])
                            t.append('_')
                    else:
                        t.append("00")
                        t.append('_')
                    # t.append(temp[2])
                    # t.append('_')
                    # t.append(temp[3])
                    # t.append('_')
                    # t.append(temp[4])
                ti = ''.join(t[:len(t)-1])
                item['time'][k] = ti
                k = k + 1

            #njudata = dict({'content': item['content'][0], 'url': item['url'], 'time': item['time'][0], 'authid': item['authid'][0],
             #               'html': item['html'], 'source': item['source'], 'source_url': item['source_url'],
              #              'n_click': item['n_click'], 'n_reply': item['n_reply'],
               #             'attention': item['attention'], 'sentiment': item['sentiment'],
                #            'title': item['title'], 'create_time': item['create_time']})

            #data = dict({'t': item['time'][0], 'au': item['authid'][0]})
            #if (self.bf.is_element_exist(str(data)) == False):
             #   self.bf.insert_element(str(data))
              #  self.collection.insert(njudata)

            i = 0
            ii = 0

            for t in item['content']:
                time_ = item['time'][i]
                authid_ = item['authid'][ii]

                njudata = dict(
                    {'content': t, 'url': item['url'], 'time': time_, 'authid': authid_, 'html': item['html'],
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


        #self.collection.insert(dict(item))
        return item
