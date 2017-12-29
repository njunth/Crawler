# -*- coding: UTF-8 -*-
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from base.items.chinakaoyanluntan.items import ChinakaoyanluntanItem
# from base.items.chinakaoyanluntan.bloomfliter import BloomFilter
from datetime import datetime
import os, random, time
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class ChinakaoyanluntanSpider(Spider):
    name = 'spider'
    allowed_domains=["chinakaoyan.com"]


    def __init__(self, name=None, **kwargs):

        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

        #self.bf=BloomFilter(0.0001,100000)
        self.mainpage="http://www.chinakaoyan.com/club/clubHome/clubId/214.shtml"


    def start_requests(self):
        while 1:
            yield Request(self.mainpage,callback=self.parse_mainPage, dont_filter=True)

    def parse_inPage(self,response):
        r1 = '.*/club/topicShow/clubId/[0-9]*/tid.*'
        sleep_time = random.random()
        print sleep_time
        time.sleep( sleep_time )
        url = response.url
        item =ChinakaoyanluntanItem()
        content_div = response.selector.xpath('//div[@class="yq11n"]')
        content1=content_div.xpath('string(.)').extract()
        try:
            if (re.match(r1, url) and len(content_div)>0):
                item['source']="中国考研网论坛"
                item['source_url']='http://www.chinakaoyan.com/'
                item['url']=url
                item['html']=response.body.decode("unicode_escape")
                click_reply_str=response.selector.xpath("//h6/text()").extract()[0]
                ccrr = re.findall(r'(\w*[0-9]+)\w*',click_reply_str)
                if(len(ccrr)>0):
                    item['n_click']=int(ccrr[0])
                else:
                    item['n_click']=0
                # print item['n_click']
                if(len(ccrr)>1):
                    item['n_reply']=int(ccrr[1])
                else:
                    item['n_reply']=0
                content1.pop()
                item['content'] = content1
                item['title'] = response.selector.xpath("//title/text()").extract()[0]
                item['attention'] = 0
                time_str=response.selector.xpath("//div[@class='yq11h']/text()").extract()
                item['time']=time_str
                authid_str=response.selector.xpath("//td[@rowspan='2']/text()").extract()
                item['authid']=authid_str
                item['sentiment']=0
                item['create_time']=str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
                yield item
        except:
            print('error')
        for t in response.selector.xpath("//a[@href]/@href").extract():
            if not t.startswith('http'):
                t="http://www.chinakaoyan.com"+t
            yield Request(t,callback=self.parse_inPage, dont_filter=True)

    def parse_mainPage(self,response):
        sel=Selector(response)
        sites=sel.xpath("//a[@href]/@href").extract()
        # while(1):
        for site in sites:
            if not site.startswith('http'):
                urls = "http://www.chinakaoyan.com"+site
            else:
                urls=site
            yield Request(urls,callback=self.parse_inPage, dont_filter=True)
            # yield Request( "http://www.chinakaoyan.com/club/clubHome/clubId/214.shtml", callback=self.parse_mainPage, dont_filter=True)