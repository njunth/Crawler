# -*- coding: utf-8 -*-
import scrapy
import re
import sys
import datetime, random, time

from base.items.tencent_menhu.items import TencentScrapyItem
from base.items.tencent_menhu.bloomfilter import BloomFilter
class DmozSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["qq.com"]
    start_urls = [
        "http://www.qq.com"
    ]
    bf = BloomFilter(0.0001, 1000000)
    r1 = '^http://.*.qq.*'
    r2 = '^http://.*.qq.*.htm.*'
    r3 = '^http://.*.qq.com/a/.*'
    r4 = '^http://.*v.qq.*'
    r5='^http://.*auto.qq.*'
    r6 = '^http://.*.qq.*.htm$'
    r7 = '^http://.*inews.qq.*'
    r8='^http://.*class.qq.*'
    def parse_inpage(self, response):

        url = response.url
        self.bf.insert_element(url)
        #print url
        sleep_time = random.random()
        print sleep_time
        time.sleep(sleep_time)
        try:
            if re.match(self.r3, url):
               # with open('aa', 'ab') as f:
                   # f.write(url + '\n')
                #print "aaaaaaa!!!!!!!@*#()@_______"
                #for sel in response:
                item = TencentScrapyItem()
                # item['name'] = sel.xpath("h1[@class='main-title']/text()").extract()[0].encode('utf-8')
                # name= item['name']
                item['title'] = response.xpath("//head/title/text()").extract_first().encode('utf-8')
                # item['title'] = response.xpath("//h1/text()").extract_first().encode('utf-8')
                #try:
                item['content'] = response.xpath("//div[@id='content']//p/text() ").extract()
                if item['content'] is None:
                    item['content'] = response.xpath("//div[@class='main']//p/text() ").extract()
                #except:
                    #item['content'] = response.xpath("//div[@id='contentText']//p/text() ").extract()
                item['content'] = ''.join(item['content'])
                # name= item['name']
                item['url'] = url
                item['sentiment'] = 0
                item['attention'] = 0

                item['html'] = ''

                contentlist = response.xpath('//html').extract()
                for con in contentlist:
                    utfcontent = con.encode('utf-8')
                    item['html'] += utfcontent

                item['source'] = "腾讯网"
                item['source_url'] = "http://www.qq.com/"

                # time_item = []
                try:
                    publish_time = response.xpath("//span[@class='article-time']/text()").extract()[0]
                except:
                    try:
                        publish_time = response.xpath("//span[@class='a_time']/text()").extract()[0]
                    except:
                        try:
                            publish_time= response.xpath("//span[@class='pubTime']/text()").extract()[0]
                        except:
                            try:
                                publish_time = response.xpath("//div[@id='time_source']/span/text()").extract()[0]
                            except:
                                publish_time = response.xpath("//span[@class='pubTime article-time']/text()").extract()[0]



                #print publish_time
                # print '\n'
                #print url
                time_item = publish_time[0:4]
                #print time_item
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
                item['create_time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                if item['content']:
                    yield item
                    #with open('aaaa', 'ab') as f:
                        #f.write(url + '\n')
        except:
            #print url
            #print '\n'
            #print(sys.exc_info())
            #print('error')
            #with open('a', 'ab') as f:
                #f.write(url + '\n')
            pass

    def parse(self, response):
        #with open('aaaaa', 'ab') as f:
            #f.write(response.url + '\n')
        for url in response.selector.xpath("//a/@href").re(self.r1):
            #print url+'\n'

            if re.match(self.r4,url)is None and re.match(self.r5,url) is None and re.match(self.r7,url) is None and re.match(self.r8,url) is None:
                if re.match(self.r3, url):
                    if (self.bf.is_element_exist(url) == False):
                        yield scrapy.Request(url=url, callback=self.parse_inpage,priority=1, dont_filter=True)

                else:
                    #with open('aa', 'ab') as f:
                     #f.write(url+'\n')
                    yield scrapy.Request(url=url, callback=self.parse,priority=0, dont_filter=True)
