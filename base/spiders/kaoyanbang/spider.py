# -*- coding: UTF-8 -*-
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from base.items.kaoyanbang.items import KaoyanbangItem
from base.items.kaoyanbang.bloomfliter import BloomFilter
from datetime import datetime
import os, random, time
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class KaoyanbangSpider(Spider):
    name = 'spider'
    allowed_domains=["kaoyan.com"]


    def __init__(self, name=None, **kwargs):

        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

        self.bf=BloomFilter(0.0001,100000)
        self.mainpage="http://www.kaoyan.com/"


    def start_requests(self):
        yield Request(self.mainpage,callback=self.parse_mainPage, dont_filter=True)

    def parse_inPage(self,response):
        sleep_time = random.random()
        print 5*sleep_time
        time.sleep( 5*sleep_time )
        r1 = '.*/zhaosheng/.+.html'
        r2 = '.*/xinwen/.+.html'
        url = response.url
        self.bf.insert_element(url)
        item =KaoyanbangItem()
        content_div = response.selector.xpath('//div[@class="article"]')
        content1=content_div.xpath('string(.)').extract()
        try:
            if (((re.match( r1, url ) or re.match( r2, url )) and len( content_div ) > 0)):
            # if (((re.match(r1, url) or re.match(r2, url))and len(content_div)>0) and (str(url).find("index")==-1)) :
                item['source']="考研帮"
                item['source_url']='http://www.kaoyan.com/'
                item['url']=url
                print item['url']
                item['html']=response.body
                i=0
                for t in content1:
                    tt = t.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
                    content1[i]=tt
                    i=i+1
                item['content'] = "".join(content1)
                item['title'] = response.selector.xpath("//title/text()").extract()[0]
                item['attention'] = 0
                time_str=response.selector.xpath("//div[@class='articleInfo']//span/text()").extract()[0]
                try:
                    item['time'] =time_str.replace('-','_').replace(' ','_').replace(':','_')
                except:
                    item['time']='0000_00_00_00_00'
                item['time']=item['time']+'_00'
                item['sentiment']=0
                item['create_time']=str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
                yield item
        except:
            print('error')
        for t in response.selector.xpath("//a[@href]/@href").extract():
            if not t.startswith('http'):
                t="http://www.kaoyan.com"+t
            if (self.bf.is_element_exist(t)==False):  # reduce a /
                yield Request(t,callback=self.parse_inPage, dont_filter=True)
            else:
                continue

    def parse_mainPage(self,response):
        sel=Selector(response)
        sites=sel.xpath("//a[@href]/@href").extract()
        while(1):
            for site in sites:
                if not site.startswith('http'):
                    urls = "http://www.kaoyan.com"+site
                else:
                    urls=site
                # print urls
                if(self.bf.is_element_exist(urls)==False):
                    yield Request(urls,callback=self.parse_inPage, dont_filter=True)
                else:
                    continue
            yield Request( self.mainpage, callback=self.parse_mainPage, dont_filter=True)
