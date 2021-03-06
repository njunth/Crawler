# -*- coding: utf-8 -*-
import os

import pytz
import scrapy
import re
import sys
from base.items.yangguang_menhu.items import YangguangMenhuItem
# from base.items.yangguang_menhu.bloomfilter import BloomFilter
import pyreBloom
from base.configs.settings import REDIS_HOST, REDIS_PORT
import datetime, random, time

class DmozSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["cnr.cn"]
    start_urls = [
        "http://www.cnr.cn/"
    ]
    # os.environ["all_proxy"] = "http://dailaoshi:D9xvyfrgPwqBx39u@bh21.84684.net:21026"
    bf = pyreBloom.pyreBloom('yangguangwang', 100000, 0.0001, host=REDIS_HOST,port=REDIS_PORT)
    tz = pytz.timezone( 'Asia/Shanghai' )
    r1 = '^http://.*.cnr.*'
    r2 = '^http://.*.cnr.*.shtml.*'
    r3 = '^http://.*.cnr.*.html.*'
    r4 = '^http://.*.cnr.*.htm.*'

    def parse_inpage(self, response):
        sleep_time = random.random()
        # print 5 * sleep_time
        time.sleep( 5 * sleep_time )
        url = response.url
        # print url
        if re.match(self.r2, url) or re.match(self.r3, url)or re.match(self.r4, url):
            try:
                # print url
                self.bf.extend(url)
                #print "aaaaaaa!!!!!!!@*#()@_______"
                #for sel in response:
                item = YangguangMenhuItem()
                # item['name'] = sel.xpath("h1[@class='main-title']/text()").extract()[0].encode('utf-8')
                # name= item['name']
                item['url'] = url
                print item['url']

                item['title'] = response.xpath("//head/title/text()").extract_first()


                #print "qqqqqq"
                item['source'] = "央广网"
                item['source_url'] = "http://www.cnr.cn/"

                #try:
                item['html'] = ''
                contentlist = response.xpath('//html').extract()
                # for con in contentlist:
                #     utfcontent = con.encode('utf-8')
                #     item['html'] += utfcontent
                #except:
                #item['html'] = response.body

                try:
                    item['content'] = response.xpath("//div[@class='TRS_Editor']//p/text()").extract()
                except:
                    item['content'] = response.xpath("//div[@class='TRS_Editor']//strong/text()").extract()
                    

                item['content'] = ''.join(item['content'])


                # time_item = []
                publish_time = response.xpath("//body//div[@class='source']/span/text()").extract()[0]
                #time1 = response.xpath("//body//div[@class='source']/span").extract()
                # time1 = response.xpath("//head/meta[@property='article:published_time']//@content").extract()[1]

                # print time

                #print time1
                #print '/n'

                time_item = publish_time[0:4]
                time_item += '_'
                time_item += publish_time[5:7]
                time_item += '_'
                time_item += publish_time[8:10]
                time_item += '_'
                time_item += publish_time[11:13]
                time_item += '_'
                time_item += publish_time[14:16]
                # time_item = ''.join(time_item)
                if len(time_item) == 16:
                    time_item += '_00'
                if len(time_item) == 17:
                    time_item += '00'
                if len(time_item) == 18:
                    time_item += '0'
                item['time'] = time_item

                item['sentiment'] = 0
                item['attention'] = 0
                # print name
                #with open('aaa', 'ab') as f:
                    #f.write(response.url)
                    #f.write('\n')
                item['create_time'] = datetime.datetime.now(self.tz).strftime('%Y_%m_%d_%H_%M_%S')
                yield item

            except:
                #print(sys.exc_info())
                pass

    def parse(self, response):
                """
                with open('aaaa', 'ab') as f:
                    f.write(response.url)
                    f.write('\n')
                    """
                for url in response.selector.xpath("//a/@href").re(self.r1):
                    # print url
                    if re.match(self.r2, url) is None and re.match(self.r3, url) is None and re.match(self.r4, url) is None:
                            yield scrapy.Request(url=url, callback=self.parse,priority=0, dont_filter=True)
                    else:
                        if (self.bf.contains(url) == False):
                            yield scrapy.Request(url=url, callback=self.parse_inpage,priority=1, dont_filter=True)

                # yield scrapy.Request(url='http://www.cnr.cn/', callback=self.parse,priority=0, dont_filter=True)

