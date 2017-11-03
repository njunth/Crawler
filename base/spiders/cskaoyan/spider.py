# -*- coding: UTF-8 -*-
from scrapy.spiders import Spider  
from scrapy.http import Request  
from scrapy.selector import Selector  
from base.items.cskaoyan.items import CskaoyanItem
from base.items.cskaoyan.bloomfliter import BloomFilter
import os


class CKYSpider(Spider):
    name = 'spider'
    allowed_domains=["cskaoyan.com"]


    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

        self.bf=BloomFilter(0.0001,100000)
        self.mainpage="http://www.cskaoyan.com/forum.php"
        self.count=0


    def start_requests(self):
        yield Request(self.mainpage,callback=self.parse_mainPage)


    def parse_inPage(self,response):
        sel=Selector(response)
        site=sel
        url=''
        item=CskaoyanItem()
        item["origion"]="cskaoyan"
        item["source_url"]="http://www.cskaoyan.com/forum-21-1.html"
        item["content"]=''
        item['current_url']=''
        currentUrl=response.url
        self.bf.insert_element(currentUrl)
       # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
       # print str(response.url)
        item['current_url'] = str(response.url)
		
        contentList=site.xpath("//*").extract()
        for floor in contentList:
            utfcontent=floor.encode('utf-8')
            item['content'] += utfcontent
            item['content'] += "\n"
        print item['content']
     #   os.system("pause")
			
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
