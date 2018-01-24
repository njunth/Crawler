# -*- coding: UTF-8 -*-
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from base.items.hongyikaoyanluntan.items import HongyikaoyanluntanItem
from base.items.hongyikaoyanluntan.bloomfliter import BloomFilter
from datetime import datetime
import random, time
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class HongyikaoyanluntanSpider(Spider):
    name = 'spider'
    allowed_domains=['hykaoyan.org']

    def __init__(self, name=None, **kwargs):

        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

        self.mainpage="http://www.hykaoyan.org/"

    def start_requests(self):
        os.environ["all_proxy"] = "http://dailaoshi:D9xvyfrgPwqBx39u@bh21.84684.net:21026"
        yield Request(self.mainpage,callback=self.parse_mainPage, dont_filter=True)

    def parse_inPage(self,response):
        sleep_time = random.random()
        print sleep_time
        time.sleep( sleep_time )
        r1 = 'http://www.hykaoyan.org/thread-[0-9]+-[0-9]+-[0-9]+.html'
        url = response.url
        item =HongyikaoyanluntanItem()
        content_div = response.selector.xpath('//table[@cellspacing="0" and @cellpadding="0"]//tr//td[@class="t_f"]')
        content1=content_div.xpath('string(.)').extract()
        try:
            if (re.match(r1, url) and len(content1)>0):
                item['source']="弘毅考研论坛"
                item['source_url']='http://www.hykaoyan.org/'
                item['url']=url
                # item['html']=response.body
                item['html'] = ''
                item['content'] = content1
                item['title'] = response.selector.xpath("//title/text()").extract()[0]
                item['attention'] = 0
                time_str=response.selector.xpath("//em[@id]/text()").extract()
                item['time']=time_str
                click1 = response.selector.xpath("//span[@class='xi1']/text()").extract()
                if(len(click1)>0): item['n_click'] = int(click1[0])
                else:item['n_click']=0
                reply1 = response.selector.xpath("//span[@class='xi1']/text()").extract()
                if(len(click1)>1): item['n_reply'] = int(click1[1])
                else:item['n_reply']=0
                item['sentiment']=0
                authid_str=response.selector.xpath("//div[@class='authi']//a[@class='xw1']/text()").extract()
                item['authid']=authid_str
                item['create_time']=str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
                yield item
        except:
            print('error')
        for t in response.selector.xpath("//a[@href]/@href").extract():
            if not t.startswith('http'):
                t="http://www.hykaoyan.org/"+t
            yield Request(t,callback=self.parse_inPage, dont_filter=True)

    def parse_mainPage(self,response):
        sel=Selector(response)
        sites=sel.xpath("//a[@href]/@href").extract()
        while(1):
            for site in sites:
                if not site.startswith('http'):
                    urls = "http://www.hykaoyan.org"+site
                else:
                    urls=site
                yield Request(urls,callback=self.parse_inPage, dont_filter=True)
