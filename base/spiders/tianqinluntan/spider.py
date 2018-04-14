# -*- coding: UTF-8 -*-
import pytz
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from base.items.tianqinluntan.items import TianqinluntanItem
# from base.items.tianqinluntan.bloomfliter import BloomFilter
from datetime import datetime
import pyreBloom
from base.configs.settings import REDIS_HOST, REDIS_PORT
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
        self.bf= pyreBloom.pyreBloom('tianqinluntan', 100000, 0.0001, host=REDIS_HOST,port=REDIS_PORT)
        self.tz = pytz.timezone( 'Asia/Shanghai' )

    def start_requests(self):
        os.environ["all_proxy"] = "http://dailaoshi:D9xvyfrgPwqBx39u@bh21.84684.net:21026"
        while 1:
            yield Request(self.mainpage,callback=self.parse_mainPage, dont_filter=True)
            # time.sleep( 60 )

    def parse_inPage(self,response):
        print response

        sleep_time = random.random()
        print sleep_time
        time.sleep( sleep_time )

        r1 = 'http://www.csbiji.com/thread-[0-9]+-[0-9]+-[0-9]+.html'
        url = response.url
        item =TianqinluntanItem()
        # print url
        content_div = response.selector.xpath('//table[@cellspacing="0" and @cellpadding="0"]//tr//td[@class="t_f"]')
        content1=content_div.xpath('string(.)').extract()
        try:
            if (re.match(r1, url) and len(content_div)>0):
                # print "crawl"
                item['source']="天勤论坛"
                item['source_url']='http://www.csbiji.com/'
                item['url']=url
                print item['url']
                # item['html']=response.body.decode("unicode_escape")
                item['html']=''
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
                item['create_time']=str(datetime.now(self.tz).strftime('%Y_%m_%d_%H_%M_%S'))
                yield item
        except:
            print('error')
        for t in response.selector.xpath("//a[@class='nxt' and @href]/@href").extract():
            if not t.startswith('http'):
                t=response.url+t
            self.bf.extend(t)
            if(self.bf.contains(t)==False):
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
            # print urls
            yield Request(urls,callback=self.parse_inPage, dont_filter=True)
        for site in sites2:
            if not site.startswith('http'):
                urls = "http://www.csbiji.com/"+site
            else:
                urls=site
            self.bf.extend(urls)
            if(self.bf.contains(urls)==False):
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
                # print urls
                yield Request(urls,callback=self.parse_zhuye, dont_filter=True)
