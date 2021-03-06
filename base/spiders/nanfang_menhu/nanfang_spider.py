# -*- coding: utf-8 -*-
import pytz
import scrapy
import re, os
import sys
from base.items.nanfang_menhu.items import NanfangScrapyItem
# from base.items.nanfang_menhu.bloomfilter import BloomFilter
import pyreBloom
import datetime, random, time
from base.configs.settings import REDIS_HOST, REDIS_PORT


class DmozSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["infzm.com"]
    start_urls = [
        "http://www.infzm.com/"
    ]
    # bf = BloomFilter(0.0001, 1000000)
    bf = pyreBloom.pyreBloom( 'nanfang_menhu', 100000, 0.0001, host=REDIS_HOST, port=REDIS_PORT )
    r1 = '^http://.*.infzm.*'
    r2='^.*content.*'
    tz = pytz.timezone( 'Asia/Shanghai' )

    def start_requests(self):
        # os.environ["all_proxy"] = "http://dailaoshi:D9xvyfrgPwqBx39u@bh21.84684.net:21026"
        while 1:
            yield scrapy.Request("http://www.infzm.com/", callback=self.parse_mainpage)

    def parse_inpage(self, response):
        url = response.url

        sleep_time = random.random()
        # print sleep_time
        #print url
        time.sleep( sleep_time )

        if re.match(self.r1,url):
            try:
                #print url
                self.bf.extend(url)
                #print "aaaaaaa!!!!!!!@*#()@_______"
                #for sel in response:
                item = NanfangScrapyItem()
                # item['name'] = sel.xpath("h1[@class='main-title']/text()").extract()[0].encode('utf-8')
                # name= item['name']
                item['url'] = url
                print url
                item['title'] = response.xpath("//head/title/text()").extract_first()



                item['source'] = "南方周末"
                item['source_url'] = "http://www.infzm.com/"

                #try:
                item['html'] = ''
                contentlist = response.xpath('//html').extract()
                for con in contentlist:
                    utfcontent = con.encode('utf-8')
                    item['html'] += utfcontent
                #except:
                #item['html'] = response.body


                item['content'] = response.xpath("//article//p//text()").extract()


                #if len(item['content'])==0:
                    #item['content'] = response.xpath("//div[@class='video_bo']//p/text()").extract()


                item['content'] = ''.join(item['content'])


                time_item = []
                try:
                    publish_time1 = response.xpath("//em[@class='pubTime']/text()").extract()[0]
                except:
                    publish_time1 = response.xpath("//p[@class='articleInfo']/text()").extract()[0]
                #print url
                #print publish_time1
                #publish_time1=''.join(publish_time1)
                #if len(publish_time1)==0:
                    #print 'aaaaaaaaaaaa'
                    #publish_time1 = response.xpath("//div[@class='video_info_left']/span/text()").extract()[0]
                

                #print publish_time1
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
                #with open('aaaa', 'ab') as f:
                    #f.write(response.url+'\n')
                #print(sys.exc_info())
                #with open('aa', 'ab') as f:
                    #f.write(response.url + '\n')
                pass

    def parse_mainpage(self, response):

                #with open('a', 'ab') as f:
                    #f.write(response.url)
                    #f.write('\n')

                for url in response.selector.xpath("//a/@href").re(self.r1):
                        if re.match(self.r2, url):
                                if (self.bf.contains(url) == False):
                                    yield scrapy.Request(url=url, callback=self.parse_inpage,priority=1)
                        else:
                            yield scrapy.Request(url=url, callback=self.parse_mainpage, priority=0)
