#encoding=utf-8
import random
import re
import sys
import time
import pyreBloom
import os
# from base.items.Bloomfilter import BloomFilter
from datetime import datetime

import pytz
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spider import Spider

from base.items.chinakaoyan.bloomfliter import BloomFilter
from base.items.chinakaoyan.items import ChinakaoyanItem
from base.configs.settings import REDIS_HOST, REDIS_PORT

reload(sys)
sys.setdefaultencoding('utf-8')


class ChinakaoyanSpider(Spider):
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
        self.tz = pytz.timezone( 'Asia/Shanghai' )
        self.bf=pyreBloom.pyreBloom('chinakaoyan', 100000, 0.0001, host=REDIS_HOST,port=REDIS_PORT)
        self.mainpage="http://www.chinakaoyan.com/info/main/ClassID/2.shtml"
        os.environ["all_proxy"] = "http://dailaoshi:D9xvyfrgPwqBx39u@bh21.84684.net:21026"


    def start_requests(self):
        while 1:
            print self.mainpage
            yield Request(self.mainpage,callback=self.parse_mainPage, dont_filter=True)

    def parse_inPage(self,response):
        sleep_time = random.random()
        # print sleep_time
        time.sleep( sleep_time )
        r1 = '.*/info/article/id.*'
        url = response.url
        self.bf.extend(url)
        item =ChinakaoyanItem()
        content_div = response.selector.xpath('//font[@face="Arial"]')
        content1=content_div.xpath('string(.)').extract()
        try:
            if (re.match(r1, url) and len(content_div)>0):
                print url
                item['source']="中国考研网"
                item['source_url']='http://www.chinakaoyan.com/'
                item['url']=url
                item['html']=''
                # item['html']=response.body.decode("unicode_escape")
                item['content'] = "".join(content1)

                item['title'] = response.selector.xpath("//title/text()").extract()[0]
                item['attention'] = 0
                time_str=response.selector.xpath("//div[@class='time']/text()").extract()[0]
                # print 111
                try:
                    time_str1 = re.search(r'\d{4}-\d+-\d+',time_str).group(0)
                    item['time'] =time_str1.replace('-','_').replace(' ','_').replace(':','_')
                    item['time']=item['time']+'_00_00_00'
                except:
                    item['time']='0000_00_00_00_00_00'
                item['sentiment']=0
                item['create_time']=str(datetime.now(self.tz).strftime('%Y_%m_%d_%H_%M_%S'))
                yield item
        except:
            print('error')
        for t in response.selector.xpath("//a[@href]/@href").extract():
            if not t.startswith('http'):
                t="http://www.chinakaoyan.com"+t
            if (self.bf.contains(t)==False):  # reduce a /
                yield Request(t,callback=self.parse_inPage, dont_filter=True)
            else:
                continue


    def parse_mainPage(self,response):
        sel=Selector(response)
        sites=sel.xpath("//a[@href]/@href").extract()
        # while (1):
        if 1==1:
            for site in sites:
                # print site
                if not site.startswith('http'):
                    urls = "http://www.chinakaoyan.com"+site
                else:
                    urls=site
                # print urls
                if(self.bf.contains(urls)==False):
                    # print urls
                    yield Request(urls,callback=self.parse_inPage, dont_filter=True)
                else:
                    continue
            # yield Request('http://www.chinakaoyan.com/info/main/ClassID/2.shtml', callback=self.parse_mainPage, dont_filter=True)
