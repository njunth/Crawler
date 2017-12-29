# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
# from scrapy.conf import settings
from base.configs.kaidi.settings import MONGO_HOST, MONGO_PORT, MONGODB_DBNAME, MONGODB_COLLECTION
from scrapy.exceptions import DropItem
import os
import re
# from base.items.kaidi.bloomfilter import BloomFilter
import pyreBloom
from base.configs.settings import REDIS_HOST, REDIS_PORT


class TencentPipeline(object):
    def __init__(self):
        self.bf = pyreBloom.pyreBloom( 'kaidi', 100000, 0.0001, host=REDIS_HOST, port=REDIS_PORT )
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
            j = 0

            # item['authid'][0] = item['mainauth']
            for v in item['authid']:
                item['authid'][j] = v
                j = j + 1

            k = 0

            for s in item['time']:
                #t = []
                # item['testtime'][k] = re.findall(r'(\w*[0-9]+-[0-9]+-[0-9]+)\w*', s)[0]
                # item['testtime'][k] = \
                temp = re.findall(r'(\w*[0-9]+/[0-9]+/[0-9]+ [0-9]+:[0-9]+:[0-9]+)\w*', s)
                if temp is not None and temp is not '':
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
                    #tem.append('_')
                    tem = ''.join(tem)
                    item['time'][n] = tem
                    n = n + 1


            njudata = dict({'content': item['content'], 'url': item['url'], 'time': item['testtime'], 'authid': item['authid'][0],
                            'html': item['html'], 'source': item['source'], 'source_url': item['source_url'],
                            'n_click': item['n_click'], 'n_reply': item['n_reply'],
                            'attention': item['attention'], 'sentiment': item['sentiment'],
                            'title': item['title'],'create_time':item['create_time']})


            data = dict({'t': item['testtime'], 'au': item['authid'][0]})
            if (self.bf.contains(str(data)) == False):
                self.bf.extend(str(data))
                self.collection.insert(njudata)


            i = 0
            ii = 0
            #for con in item['content']:
             #   item['replies'].append(con)
            for t in item['replies']:

                time_ = item['time'][i]
                authid_ = item['authid'][ii]

                njudata = dict(
                    {'content': t, 'url': item['url'], 'time': item['time'][i], 'authid': authid_, 'html': item['html'],
                     'source': item['source'], 'source_url': item['source_url'], 'n_click': item['n_click'],
                     'n_reply': item['n_reply'], 'attention': item['attention'], 'sentiment': item['sentiment'],
                     'title': item['title'],'create_time':item['create_time']})

                i = i + 1
                ii = ii + 1

                data = dict({'t': time_, 'au': authid_})
                if (self.bf.contains(str(data)) == False):
                    self.bf.extend(str(data))
                    self.collection.insert(njudata)
                #self.collection.insert(dict(njudata))

        return item

