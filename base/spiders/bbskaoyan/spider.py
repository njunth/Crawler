# -*- coding: UTF-8 -*-
from scrapy.spider import Spider  
from scrapy.http import Request  
from scrapy.selector import Selector  
from base.items.bbskaoyan.items import BbskaoyanItem
from base.items.bbskaoyan.bloomfliter import BloomFilter
import os


class BKYSpider(Spider):
    name = 'spider'
    allowed_domains=["bbs.kaoyan.com"]


    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

        self.bf=BloomFilter(0.0001,100000)
        self.mainpage="http://bbs.kaoyan.com/"
        self.count=0


    def start_requests(self):
        yield Request(self.mainpage,callback=self.parse_mainPage)


    def parse_inPage(self,response):
        sel=Selector(response)
        site=sel
        url=''
        item=BbskaoyanItem()
        item["origion"]="bbskaoyan"
        item["source_url"]="http://bbs.kaoyan.com/"
        item["content"]=''
        item['current_url']=str(response.url)
        currentUrl=response.url
        self.bf.insert_element(currentUrl)
        #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
        print str(response.url)
        item['current_url'] = str(response.url)
		
        #contentList=site.xpath("//*").extract()
        #for floor in contentList:
        #    utfcontent=floor.encode('utf-8')
        #    item['content'] += utfcontent
        #    item['content'] += "\n"
        #print item['content']
        #os.system("pause")
        item['content']=response.body
        print item['content']
        print item['current_url']
       # os.system("pause")
			
        current_urlrlList=str(response.url)
        yield item

        urlList=site.xpath("//*[@href]/@href").extract()
        for t in urlList:
            if not t.startswith('http'):
                t=response.url+t
            if (self.bf.is_element_exist(t)==False):  # reduce a /
                yield Request(t,callback=self.parse_inPage)
            else:
                continue

        self.count+=1
        yield Request(self.mainpage,callback=self.parse_mainPage)


    def parse_mainPage(self,response):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
       # system("pause")
        print str(response.url)
        sel=Selector(response)
        sites=sel.xpath("//*[@href]/@href").extract()
        for site in sites:
            if not site.startswith('http'):
                urls = response.url+site
            else:
                urls=site;
            if(self.bf.is_element_exist(urls)==False):
                yield Request(urls,callback=self.parse_inPage)
            else:
                continue
