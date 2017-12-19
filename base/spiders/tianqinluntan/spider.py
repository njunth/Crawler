# -*- coding: UTF-8 -*-
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from base.items.tianqinluntan.items import TianqinluntanItem
from base.items.tianqinluntan.bloomfliter import BloomFilter
from datetime import datetime
import os, random, time
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class TianqinluntanSpider(Spider):
    name = 'spider'
    #allowed_domains=["csbiji.com"]


    def __init__(self, name=None, **kwargs):

        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []
        self.mainpage="http://www.csbiji.com/forum.php"
        self.bf=BloomFilter(0.0001,100000)

    def start_requests(self):
        while 1:
            yield Request(self.mainpage,callback=self.parse_mainPage, dont_filter=True)
            time.sleep( 60 )

    def parse_inPage(self,response):
        

        sleep_time = random.random()
        print sleep_time
        time.sleep( sleep_time )

        r1 = 'http://www.csbiji.com/thread-[0-9]+-[0-9]+-[0-9]+.html'
        url = response.url
        item =TianqinluntanItem()
        print url
        content_div = response.selector.xpath('//table[@cellspacing="0" and @cellpadding="0"]//tr//td[@class="t_f"]')
        content1=content_div.xpath('string(.)').extract()
        try:
            if (re.match(r1, url) and len(content_div)>0):
                print "crawl"
                item['source']="天勤论坛"
                item['source_url']='http://www.csbiji.com/'
                item['url']=url
                item['html']=response.body.decode("unicode_escape")
                # item['html']=''
                click1 = response.selector.xpath("//span[@class='xi1']/text()").extract()
                if(len(click1)>0): item['n_click'] = int(click1[0])
                else:item['n_click']=0
                reply1 = response.selector.xpath("//span[@class='xi1']/text()").extract()
                if(len(click1)>1): item['n_reply'] = int(click1[1])
                else:item['n_reply']=0
                item['content'] = content1
                item['title'] = response.selector.xpath("//h1[@class='ts']//a[@id='thread_subject']/text()").extract()[0]
                item['attention'] = 0
                time_str=response.selector.xpath("//em[@id]/text()").extract()
                item['time']=time_str
                authid_str=response.selector.xpath("//div[@class='authi']//a[@class='xw1']/text()").extract()
                item['authid']=authid_str
                item['sentiment']=0
                item['create_time']=str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
                yield item
        except:
            print('error')
        for t in response.selector.xpath("//a[@class='nxt' and @href]/@href").extract():
            if not t.startswith('http'):
                t=response.url+t
            self.bf.insert_element(t)
            if(self.bf.is_element_exist(t)==False):
                yield Request(t,callback=self.parse_inPage, dont_filter=True)
            else:
                continue

    def parse_zhuye(self,response):
        sel=Selector(response)
        sites=sel.xpath("//th[@class='common']//a[@href]/@href").extract()
        sites2=sel.xpath("//a[@class='nxt' and @href]/@href").extract()
        for site in sites:
            if not site.startswith('http'):
                urls = "http://www.csbiji.com/"+site
            else:
                urls=site
            yield Request(urls,callback=self.parse_inPage)
        for site in sites2:
            if not site.startswith('http'):
                urls = "http://www.csbiji.com/"+site
            else:
                urls=site
            self.bf.insert_element(urls)
            if(self.bf.is_element_exist(urls)==False):
                yield Request(urls,callback=self.parse_zhuye, dont_filter=True)
            else:
                continue


    def parse_mainPage(self,response):
        sel=Selector(response)
        sites=sel.xpath("//div[@class='fl_icn_g']//a[@href]/@href").extract()
        while(1):
            for site in sites:
                if not site.startswith('http'):
                    urls = "http://www.csbiji.com/"+site
                else:
                    urls=site
                yield Request(urls,callback=self.parse_zhuye, dont_filter=True)
