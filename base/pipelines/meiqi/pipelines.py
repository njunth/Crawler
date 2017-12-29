# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#from base.configs.meiqi.settings import MONGODB_SERVER, MONGODB_PORT, MONGODB_DBNAME, MONGODB_COLLECTION
from scrapy import log

import pymongo
# from scrapy.conf import settings

from base.configs.meiqi.settings import MONGO_HOST, MONGO_PORT, MONGODB_DBNAME, MONGODB_COLLECTION
from scrapy.exceptions import DropItem
# from base.items.meiqi.BloomFilter import BloomFilter
import pyreBloom
from base.configs.settings import REDIS_HOST, REDIS_PORT
import re
import datetime

class MeiqiPipeline(object):
    def __init__(self):
        self.bf = pyreBloom.pyreBloom('meiqi', 100000, 0.0001, host=REDIS_HOST,port=REDIS_PORT)
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

            #item['authid'][0] = item['mainauth']
            for v in item['authid']:
                item['authid'][j] = v
                j = j + 1

                # os.system("pause")

            k = 0
            item['create_time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            for s in item['testtime']:
                # item['testtime'][k] = re.findall(r'(\w*[0-9]+-[0-9]+-[0-9]+)\w*', s)[0]
                # item['testtime'][k] = \
                temp = re.findall(r'(\w*[0-9]+)\w*', s)
                t = []
                t.append(temp[0])
                t.append('_')
                if len(temp[1]) is 1:
                    t.append('0')
                    t.append(temp[1])
                else:
                    t.append(temp[1])
                t.append('_')

                if len(temp[2]) is 1:
                    t.append('0')
                    t.append(temp[2])
                else:
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

            i = 0
            ii = -1
            for t in item['content']:

                time_ = item['testtime'][i]
                #authid_ = item['authid'][ii]

                if ii is -1:
                    njudata = dict({'content': t, 'url': item['url'], 'time': time_, 'authid': item['mainauth'], 'html': item['html'],'source': item['source'], 'source_url': item['source_url'], 'n_click': item['n_click'],'n_reply': item['n_reply'], 'attention': item['attention'], 'sentiment': item['sentiment'],'title': item['title'],'create_time':item['create_time']})
                else:
                    authid_ = item['authid'][ii]
                    njudata = dict(
                        {'content': t, 'url': item['url'], 'time': time_, 'authid': authid_, 'html': item['html'],
                         'source': item['source'], 'source_url': item['source_url'], 'n_click': item['n_click'],
                         'n_reply': item['n_reply'], 'attention': item['attention'], 'sentiment': item['sentiment'],
                         'title': item['title'],'create_time':item['create_time']})

                if ii is -1:
                    authid_ = item['mainauth']
                else:
                    authid_ = item['authid'][ii]

                i = i + 1
                ii = ii + 1


                data = dict({'t': time_, 'au': authid_})
                if (self.bf.contains(str(data)) == False):
                    self.bf.extend(str(data))
                    self.collection.insert(njudata)


            #self.collection.insert(dict(item))

        return item
