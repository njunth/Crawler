# coding=utf-8
import os

import scrapy
import re
import sys
import datetime, random, time
import pyreBloom

from base.items.ifeng_menhu.items import IfengScrapyItem
# from base.items.ifeng_menhu.bloomfilter import BloomFilter
from base.configs.settings import REDIS_HOST, REDIS_PORT


class DmozSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["ifeng.com"]
    start_urls = [
        "http://www.ifeng.com"
    ]
    bf = pyreBloom.pyreBloom('ifeng_menhu', 100000, 0.0001, host=REDIS_HOST,port=REDIS_PORT)
    os.environ["all_proxy"] = "http://dailaoshi:D9xvyfrgPwqBx39u@bh21.84684.net:21026"
    r1 = '^http://.*.ifeng.*'
    r2 = '^http://.*.ifeng.*.shtml.*'

    r4 = '^http://.*v.ifeng.*'
    r5 = '^http://.*zhibo.ifeng.*'
    r6='^http://.*art.ifeng.*'
    r7='^http://.*house.ifeng.*'
    def parse_inpage(self, response):
        sleep_time = random.random()
        # print 3*sleep_time
        time.sleep( 3*sleep_time )

        url = response.url
        self.bf.extend(url)

        try:
            if re.match(self.r2, url) :
                #with open('aaaa', 'ab') as f:
                    #f.write(url + '\n')
                #print "aaaaaaa!!!!!!!@*#()@_______"
                #for sel in response:
                item = IfengScrapyItem()
                # item['name'] = sel.xpath("h1[@class='main-title']/text()").extract()[0].encode('utf-8')
                # name= item['name']
                item['title'] = response.xpath("//head/title/text()").extract_first().encode('utf-8')
                # item['title'] = response.xpath("//h1/text()").extract_first().encode('utf-8')
                #try:
                #item['content'] = response.xpath("//div[@id='yc_con_txt']//p/text() ").extract()
                #if item['content'] is None:



                cont = response.xpath("//div[@id='main_content']//p/text()").extract()
                if len(cont)==0:
                    cont = response.xpath("//div[@class='cont']//p/text()").extract()
                if len(cont) == 0:
                    cont = response.xpath("//div[@id='picTxt']//p/text()").extract()
                #except:
                    #item['content'] = response.xpath("//div[@id='contentText']//p/text() ").extract()

                item['content'] = ''.join(cont)
                #print item['content']
                #print 'a'
                # name= item['name']
                item['url'] = url
                print url
                item['sentiment'] = 0
                item['attention'] = 0

                item['html'] = ''

                contentlist = response.xpath('//html').extract()
                # for con in contentlist:
                #     utfcontent = con.encode('utf-8')
                #     item['html'] += utfcontent

                item['source'] = u"凤凰网"
                item['source_url'] = "http://www.ifeng.com/"

                # time_item = ''
                publish_time = response.xpath("normalize-space(//p[@class='p_time']//span/text())").extract()[0]
                if len(publish_time) == 0:
                    publish_time = response.xpath("normalize-space(//div[@class='titL']//span/text())").extract()[0]
                if len(publish_time) == 0:
                    publish_time = response.xpath("normalize-space(//div[@id='artical']//span/text())").extract()[0]
                if len(publish_time) == 0:
                        #print url+'\n'
                        publish_time = response.xpath("normalize-space(//div[@class='cont']//span/text())").extract()[0]
                        if re.match("^[0-9]",publish_time) is None:
                            publish_time = response.xpath("normalize-space(//div[@id='title']/p/span[2]/text())").extract()[0]
                        time_item = publish_time[0:4]
                        time_item += '_'
                        time_item += publish_time[5:7]
                        time_item += '_'
                        time_item += time[8:10]
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
                else:
                #print time
                # print '\n'
                    time_item = publish_time[0:4]
                    time_item += '_'
                    time_item += publish_time[5:7]
                    time_item += '_'
                    time_item += publish_time[8:10]
                    time_item += '_'
                    time_item += publish_time[12:14]
                    time_item += '_'
                    time_item += publish_time[15:17]
                    # time_item = ''.join(time_item)
                    if len(time_item) == 16:
                        time_item += '_00'
                    if len(time_item) == 17:
                        time_item += '00'
                    if len(time_item) == 18:
                        time_item += '0'
                    item['time'] = time_item

                is_time = item['time'].replace('_', '')
                # print is_time
                if not is_time.isdigit():
                    item['time'] = datetime.datetime.now().strftime( '%Y_%m_%d_%H_%M_%S' )
                # print item['time']

                item['create_time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                if publish_time and item['content']:
                    yield item
                    #with open('aaaa', 'ab') as f:
                        #f.write(url + '\n')
                        #f.write(time_item + '\n')
                else:
                    pass
                    #with open('a', 'ab') as f:
                       #f.write(url + '\n')
        except:
            #print url
            #print '\n'
            #print(sys.exc_info())
            #print('error')
            #with open('a++', 'ab') as f:
                #f.write(url + '\n')
            pass

    def parse(self, response):
        #with open('aaaaa', 'ab') as f:
            #f.write(response.url + '\n')
        for url in response.selector.xpath("//a/@href").re(self.r1):
            #print url+'\n'
            if re.match(self.r4,url)is None and re.match(self.r5,url) is None and re.match(self.r7,url) is None:
                if re.match(self.r2, url):
                    if (self.bf.contains(url) == False):
                        yield scrapy.Request(url=url, callback=self.parse_inpage,priority=1, dont_filter=True)

                else:
                    #with open('aa', 'ab') as f:
                     #f.write(url+'\n')
                    yield scrapy.Request(url=url, callback=self.parse,priority=0, dont_filter=True)
            # yield scrapy.Request(url="http://www.ifeng.com", callback=self.parse,priority=0, dont_filter=True)
