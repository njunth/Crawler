# -*- coding: utf-8 -*-
import os

import pytz
import scrapy
import re
import sys
from base.items.nanfangwang_menhu.items import NanfangwangScrapyItem
# from base.items.nanfangwang_menhu.bloomfilter import BloomFilter
import pyreBloom
import datetime, random, time
from base.configs.settings import REDIS_HOST, REDIS_PORT

class DmozSpider(scrapy.Spider):
    name = "spider"
    #allowed_domains = ["bjnews.com.cn"]
    start_urls = [
        'http://www.southcn.com'
    ]
    # bf = BloomFilter(0.0001, 1000000)
    bf = pyreBloom.pyreBloom( 'nanfang_menhu', 100000, 0.0001, host=REDIS_HOST, port=REDIS_PORT )
    r1 = 'http://.*.southcn.*'
    r='.*content.*'
    r2='^http://.*.southcn.*.htm.*'
    r3='^http://.*tv.*'
    tz = pytz.timezone( 'Asia/Shanghai' )

    def start_requests(self):
        os.environ["all_proxy"] = "http://dailaoshi:D9xvyfrgPwqBx39u@bh21.84684.net:21026"
        while 1:
            yield scrapy.Request("http://www.southcn.com", callback=self.parse_mainpage)

    def parse_inpage(self, response):
        url = response.url

        sleep_time = random.random()
        # print sleep_time
        #print url
        time.sleep( sleep_time )

        if re.match(self.r1,url):
            try:
                print url
                self.bf.extend(url)
                #print "aaaaaaa!!!!!!!@*#()@_______"
                #for sel in response:
                item = NanfangwangScrapyItem()
                # item['name'] = sel.xpath("h1[@class='main-title']/text()").extract()[0].encode('utf-8')
                # name= item['name']
                item['url'] = url
                #print url
                item['title'] = response.xpath("//head/title/text()").extract_first()



                item['source'] = "中国青年报"
                item['source_url'] = "http://www.cyol.net/"

                #try:
                item['html'] = ''
                contentlist = response.xpath('//html').extract()
                for con in contentlist:
                    utfcontent = con.encode('utf-8')
                    item['html'] += utfcontent
                #except:
                #item['html'] = response.body


                item['content'] = response.xpath("//div[@class='content']//p//text()").extract()

                item['content'] = ''.join(item['content'])


                time_item = []

                #try:
                publish_time1 = response.xpath("//span[@class='pub_time']/text()").extract()[0]
                publish_time = re.findall(r'(\w*[0-9]+)\w*', publish_time1)
                publish_time=''.join(publish_time)
                if(len(publish_time)!= 0):
                    while len(publish_time)<14:
                        publish_time+='0'
                #print publish_time

                #print url
                #print publish_time
                time_item.append(publish_time[0:4])
                time_item += '_'
                time_item += publish_time[4:6]
                time_item += '_'
                time_item += publish_time[6:8]
                time_item += '_'

                time_item += publish_time[8:10]
                time_item += '_'
                time_item += publish_time[10:12]
                time_item += '_'
                time_item += publish_time[12:14]

                time_item = ''.join(time_item)
                item['time'] = time_item

                item['sentiment'] = 0
                item['attention'] = 0
                # print name
                #with open('aaa', 'ab') as f:
                    #f.write(response.url)
                    #f.write('\n')
                item['create_time'] = datetime.datetime.now(self.tz).strftime('%Y_%m_%d_%H_%M_%S')
                item['html'] = ''
                if item['content'] and item['time']:
                    #with open('aaa', 'ab') as f:
                        #f.write(response.url + '\n')
                        #f.write(item['time']+'\n')

                    yield item
                else:
                    #with open('aaaa', 'ab') as f:
                        #f.write(response.url + '\n')
                    pass

            except:
                #with open('aa', 'ab') as f:
                   # f.write(response.url+'\n')
                #print(sys.exc_info())
                #with open('aa', 'ab') as f:
                    #f.write(response.url + '\n')
                pass

    def parse_mainpage(self, response):

                #with open('a', 'ab') as f:
                    #f.write(response.url)
                    #f.write('\n')
                result = response.url.split('/')
                #print(result)
                for url in response.selector.xpath("//a/@href").re(self.r1+'|'+self.r):
                    if re.match(self.r3,url) is None:
                        if not url.startswith('http:'):
                            url = "http://" +result[2]+'/'+ url
                            #print url
                        if re.match(self.r, url) :
                                if (self.bf.contains(url) == False):
                                    yield scrapy.Request(url=url, callback=self.parse_inpage,priority=1)
                        else:
                            yield scrapy.Request(url=url, callback=self.parse_mainpage, priority=0)
