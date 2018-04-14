#-*-coding:utf8-*-
import os

import pytz
import scrapy
from base.items.yuyou.items import YuyouItem
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
# from base.items.yuyou.bloomfilter import BloomFilter
import string
import datetime, random, time

class YuyouSpider(scrapy.Spider):
    name = "spider"

    allowed_domins = ["yanjiao.com"]

    start_urls = {
        "http://pbbs.lnfisher.com/"
    }
    tz = pytz.timezone( 'Asia/Shanghai' )
    # bf = BloomFilter(0.0001,1000000)

    #r1 = '^http://pbbs.lnfisher.com/forum.php?mod=viewthread&tid=[0-9]*'
    r1 = '.*.tid*.*'
    #r1 = 'http://pbbs.lnfisher.com/forum.php?mod=viewthread&tid=[0-9]+'
    r2 = '^http://www.yanjiao.com.thread.*.[0-9]+'
    def parse(self, response):
        os.environ["all_proxy"] = "http://dailaoshi:D9xvyfrgPwqBx39u@bh21.84684.net:21026"
        r3 = '.*.thread.*'
        r4 = '^http://pbbs.lnfisher.com.*'
        r5 = r3 + '|' + r4
        while 1:
            for url1 in response.selector.xpath("//a/@href").re(r5):
                if not url1.startswith('http'):
                    url1 = "http://pbbs.lnfisher.com" + url1

                if re.match(self.r1, url1) :#or re.match(self.r2, url1):  # reduce a /
                    yield scrapy.Request(url=url1, callback=self.parse_inpage, priority=1, dont_filter=True)
                else:
                    yield scrapy.Request(url=url1, callback=self.parse, priority=1, dont_filter=True)

    def parse_inpage(self,response):
        sleep_time = random.random()
        # print sleep_time
        time.sleep( sleep_time )
        item = YuyouItem()
        content = response.selector.xpath("//td[@class='t_f']")
        con_div = content.xpath('string(.)').extract()

        #if re.match(self.r1, response.url) or re.match(self.r2, response.url):

        item['source'] = '辽宁渔友之家'
        item['source_url'] = 'http://pbbs.lnfisher.com/'

        item['html'] = ''
        contentlist = response.xpath('//html').extract()
        for con in contentlist:
            utfcontent = con.encode('utf-8')
            item['html'] += utfcontent

        item['url'] = response.url
        print item['url']
        t = response.xpath("//span[@id='thread_subject']/text()").extract()  # [0].encode('utf-8')
        title = ''.join(t)
        title1 = title.encode('utf-8')
        item['title'] = title1

        #item['content'] = response.xpath("//td[@class='t_f']//font//text()").extract()
        item['content'] = con_div
        item['authid'] = response.xpath("//div[@class='authi']//a[@class='xw1']//text()").extract()

        #item['n_click']
        n_click = response.xpath("//span[@class='xi1']//text()").extract_first()
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

        #item['n_reply']
        n_reply = response.xpath("//span[@class='xi1']//text()").extract()[1]

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

        item['testtime'] = response.xpath("//div[@class='authi']//em//span").extract()
        item['create_time'] = datetime.datetime.now(self.tz).strftime( '%Y_%m_%d_%H_%M_%S' )
        item['html'] = ''
        #item['testtime'] = response.xpath("//div[@class='authi']//em").extract()
        #item['replies'] = response.xpath("//tr//td[@class='t_f']//text()").extract()
        #item['testcontent'] = response.xpath("//td[@class='t_f']//text()").extract()
        item['sentiment'] = 0
        item['attention'] = 0

        yield item
