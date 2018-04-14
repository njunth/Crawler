# -*- coding: UTF-8 -*-
import pytz
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from base.items.okkaoyan.items import OkkaoyanItem
# from base.items.okkaoyan.bloomfliter import BloomFilter
import pyreBloom
from base.configs.settings import REDIS_HOST, REDIS_PORT
from datetime import datetime
import os, random, time
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class OkkaoyanSpider(Spider):
    name = 'spider'
    allowed_domains=["okaoyan.com"]


    def __init__(self, name=None, **kwargs):

        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

        self.bf=pyreBloom.pyreBloom('okkaoyan', 100000, 0.0001, host=REDIS_HOST,port=REDIS_PORT)
        self.tz = pytz.timezone( 'Asia/Shanghai' )
        self.mainpage="http://www.okaoyan.com/"


    def start_requests(self):
        os.environ["all_proxy"] = "http://dailaoshi:D9xvyfrgPwqBx39u@bh21.84684.net:21026"
        while 1:
            yield Request(self.mainpage,callback=self.parse_mainPage, dont_filter=True)

    def parse_inPage(self,response):
        sleep_time = random.random()
        # print sleep_time
        time.sleep( sleep_time )
        r1 = '.*html'
        url = response.url
        self.bf.extend(url)
        item =OkkaoyanItem()
        content_div = response.selector.xpath('//div[@class="article-body"]')
        content1=content_div.xpath('string(.)').extract()
        try:
            if ((re.match(r1, url)and len(content_div)>0)) :
                item['source']="OK考研"
                item['source_url']='http://www.okaoyan.com/'
                item['url']=url
                print item['url']
                # item['html']=response.body
                item['html'] = ''
                i=0
                for t in content1:
                    tt = t.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
                    content1[i]=tt
                    i=i+1
                item['content'] = "".join(content1)
                item['title'] = response.selector.xpath("//title/text()").extract()[0]
                item['attention'] = 0
                time_str=response.selector.xpath("//h2[@class='article-h2']//span/text()").extract()[0]
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
                t="http://www.okaoyan.com"+t
            if (self.bf.contains(t)==False):  # reduce a /
                yield Request(t,callback=self.parse_inPage, dont_filter=True)
            else:
                continue

    def parse_mainPage(self,response):
        sel=Selector(response)
        sites=sel.xpath("//a[@href]/@href").extract()
        # while(1):
        if 1==1:
            for site in sites:
                if not site.startswith('http'):
                    urls = "http://www.okaoyan.com"+site
                else:
                    urls=site
                if(self.bf.contains(urls)==False):
                    yield Request(urls,callback=self.parse_inPage, dont_filter=True)
                else:
                    continue
            # yield Request(self.mainpage,callback=self.parse_mainPage, dont_filter=True)
