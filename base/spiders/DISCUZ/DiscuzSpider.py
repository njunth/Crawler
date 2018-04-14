#-*-coding:utf8-*-
import os

import pytz
import scrapy
from base.items.DISCUZ.items import DiscuzItem
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from base.items.DISCUZ.bloomfilter import BloomFilter
import string
import datetime

class DiscuzSpider(scrapy.Spider):
    name = "spider"

    allowed_domins = ["discuz.net"]

    start_urls = {
        "http://www.discuz.net/forum.php"
    }
    os.environ["all_proxy"] = "http://dailaoshi:D9xvyfrgPwqBx39u@bh21.84684.net:21026"
    #bf = BloomFilter(0.0001, 1000000)
    tz = pytz.timezone( 'Asia/Shanghai' )
    def parse(self, response):
        while 1:
            for url1 in response.selector.xpath("//a/@href").re(r'^http://www.discuz.net.*'):
                if not url1.startswith('http'):
                    url1 += "http://www.discuz.net/"
                #if (self.bf.is_element_exist(url1) == False):
                yield scrapy.Request(url=url1, callback=self.parse_inpage)


    def parse_inpage(self, response):
        item = DiscuzItem()

        con = response.selector.xpath("//td[@class='t_f']")
        con1 = con.xpath('string(.)').extract()

        if re.match('^http://www.discuz.net.*',response.url) and len(con1)>0:
            item['source'] = 'Discuz论坛'
            item['source_url'] = 'http://www.discuz.net/forum.php'

            item['html'] = ''
            # contentlist = response.xpath('//html').extract()
            # for con in contentlist:
            #     utfcontent = con.encode('utf-8')
            #     item['html'] += utfcontent

            item['url'] = response.url
            #self.bf.insert_element(item['url'])

            item['sentiment'] = 0
            item['attention'] = 0
            item['create_time'] = datetime.datetime.now(self.tz).strftime('%Y_%m_%d_%H_%M_%S')
        #item['n_click'] = \
            n_click = response.xpath('//div[@class="hm ptn"]//span[@class="xi1"]/text()').extract_first()
        #item['n_reply'] \
            n_reply = response.xpath('//div[@class="hm ptn"]//span[5]/text()').extract()


            if n_click is None:
                item['n_click'] = 0
            else:
                nclick = ''.join(n_click)
                nc = nclick
                for c in string.punctuation:
                    nc = nc.replace(c, '')

                if nc is None:
                    item['n_click'] = 0
                else:
                    item['n_click'] = int(nc)

            if n_reply is None:
                item['n_reply'] = 0
            else:
                nreply = ''.join(n_reply)
                nr = nreply
                for c in string.punctuation:
                    nr = nr.replace(c, '')

                if nr is None:
                    item['n_reply'] = 0
                else:
                    if nr is '':
                        item['n_reply'] = 0
                    else:
                        item['n_reply'] = int(nr)

            item['time'] = response.xpath('//div[@class="authi"]//em/text()').extract()
            item['authid'] = response.xpath('//div[@class="authi"]//a[@class="xw1"]/text()').extract()
            #item['title'] = ''.join(item['title'])
            #item['title'] = \
            t = response.xpath('//h1[@class="ts"]//span[@id="thread_subject"]/text()').extract()
            title = ''.join(t)
            title1 = title.encode('utf-8')
            item['title'] = title1

            item['content'] = con1 #response.xpath('//td[@class="t_f"]//text()').extract()

            yield item





    #def parse_inpage(self,response):


