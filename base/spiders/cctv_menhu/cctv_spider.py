# -*- coding: utf-8 -*-
import pytz
import scrapy
import re, os
import sys
from base.items.cctv_menhu.items import CctvScrapyItem
# from base.items.cctv_menhu.bloomfilter import BloomFilter
import pyreBloom
import datetime, random, time
from base.configs.settings import REDIS_HOST, REDIS_PORT


class DmozSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["cctv.com"]
    start_urls = [
        "http://www.cctv.com"
    ]
    # bf = BloomFilter(0.0001, 1000000)
    bf = pyreBloom.pyreBloom( 'cctv_menhu', 100000, 0.0001, host=REDIS_HOST, port=REDIS_PORT )
    tz = pytz.timezone( 'Asia/Shanghai' )
    r1 = '^http://.*.cctv.*'
    r2 = '^http://.*.cctv.*.shtml.*'
    r3 = '^http://.*.cctv.*./index.*'
    r4='^http://.*.cctv.*./VID.*'

    r5='^http://english.cctv.*'
    r6 ='^http://espanol.cctv.*'
    r7 = '^http://fr.cctv.*'
    r8 = '^http://arabic.cctv.*'
    r9 = '^http://russian.cctv.*'
    r10 = '^http://mn.cctv.*'
    r11 = '^http://tibetan.cctv.*'
    r12 = '^http://mongol.cctv.*'
    r13 = '^http://uyghur.cctv.*'
    r14 = '^http://kazakh.cctv.*'
    r_language=r5+'|'+r6+'|'+r7+'|'+r8+'|'+r9+'|'+r10+'|'+r11+'|'+r12+'|'+r13+'|'+r14
    def start_requests(self):
        # os.environ["all_proxy"] = "http://dailaoshi:D9xvyfrgPwqBx39u@bh21.84684.net:21026"
        while 1:
            yield scrapy.Request("http://www.cctv.com", callback=self.parse_mainpage)
    def parse_inpage(self, response):
        url = response.url
        #print url
        sleep_time = random.random()
        print sleep_time
        time.sleep( sleep_time )
        flag=0
        if re.match(self.r2, url):
            try:
                #print url
                self.bf.extend(url)
                #print "aaaaaaa!!!!!!!@*#()@_______"
                #for sel in response:
                item = CctvScrapyItem()
                # item['name'] = sel.xpath("h1[@class='main-title']/text()").extract()[0].encode('utf-8')
                # name= item['name']
                item['url'] = url
                print url

                item['title'] = response.xpath("//head/title/text()").extract_first()


                #print "qqqqqq"
                item['source'] = "央视网"
                item['source_url'] = "http://www.cctv.com/"

                #try:
                item['html'] = ''
                contentlist = response.xpath('//html').extract()
                for con in contentlist:
                    utfcontent = con.encode('utf-8')
                    item['html'] += utfcontent
                #except:
                #item['html'] = response.body


                item['content'] = response.xpath("//div[@class='wrapper']//p/text()").extract()

                if len(item['content'])==0:
                    item['content'] = response.xpath("//div[@id='page_body']//p/text()").extract()

                if len(item['content'])==0:
                    item['content'] = response.xpath("//div[@id='content_body']//p/text()").extract()
                """
                if len(item['content']) == 0:
                    item['content'] = response.xpath("//div[@id='content']//p/text()").extract()
                if len(item['content']) == 0:
                    item['content'] = response.xpath("//div[@id='Content']//p/text()").extract()
                if len(item['content']) == 0:
                    item['content'] = response.xpath("//div[@class='zw_pic']//p/text()").extract()
                if len(item['content']) == 0:
                    item['content'] = response.xpath("//div[@class='main_content']//p/text()").extract()
                if len(item['content']) == 0:
                    item['content'] = response.xpath("//div[@class='zw']//p/text()").extract()
"""
                item['content'] = ''.join(item['content'])

                time_item = []

                #publish_time1 = response.xpath("normalize-space(//script[11]//text())").extract()
                #print url
                #print publish_time1
                #publish_time = re.findall(r'(\w*[0-9]+)\w*',publish_time1)
                publish_time = re.search(r'\"\d{14} \"', item['html']).group(0)
                #print publish_time
                print publish_time
                #print url
                #print publish_time
                time_item.append(publish_time[1:5])
                time_item += '_'
                time_item += publish_time[5:7]
                time_item += '_'
                time_item += publish_time[7:9]
                time_item += '_'
                time_item += publish_time[9:11]
                time_item += '_'
                time_item += publish_time[11:13]
                time_item += '_'
                time_item += publish_time[13:15]
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
                if publish_time and item['content']:
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

                #with open('aa', 'ab') as f:
                    #f.write(response.url)
                    #f.write('\n')

                for url in response.selector.xpath("//a/@href").re(self.r1):
                    if re.match(self.r_language, url) is None:
                        if re.match(self.r2, url) is None or re.match(self.r3, url):
                                yield scrapy.Request(url=url, callback=self.parse_mainpage,priority=0)
                        else:
                            if re.match(self.r4,url) is None:
                                if (self.bf.contains(url) == False):
                                    yield scrapy.Request(url=url, callback=self.parse_inpage,priority=1)

