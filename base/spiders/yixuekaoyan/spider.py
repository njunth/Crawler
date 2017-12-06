# -*- coding: UTF-8 -*-
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from base.items.yixuekaoyan.items import YixuekaoyanItem
from base.items.yixuekaoyan.bloomfliter import BloomFilter
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class YixuekaoyanSpider(Spider):
    name = 'spider'
    allowed_domains=["medkaoyan.net"]


    def __init__(self, name=None, **kwargs):

        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

        self.bf=BloomFilter(0.0001,100000)
        self.mainpage="http://www.medkaoyan.net/"


    def start_requests(self):
        yield Request(self.mainpage,callback=self.parse_mainPage)

    def parse_inPage(self,response):
        r1 = '.*html'
        url = response.url
        self.bf.insert_element(url)
        item =YixuekaoyanItem()
        content_div = response.selector.xpath('//div[@class="nr"]')
        content1=content_div.xpath('string(.)').extract()
        try:
            if ((re.match(r1, url)and len(content_div)>0)) :
                item['source']='yixuekaoyan'
                item['source_url']='http://www.medkaoyan.net/'
                item['url']=url
                item['html']=''
                i=0
                for t in content1:
                    tt = t.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
                    content1[i]=tt
                    i=i+1
                item['content'] = "".join(content1)
                item['title'] = response.selector.xpath("//title/text()").extract()[0]
                time_str=response.selector.xpath("//div[@class='nrx']/text()").extract()[0]
                try:
                    item['time'] = re.search(r'\d{4}-\d+-\d+',time_str).group(0)
                except:
                    item['time']='no time'
                item['attention'] = 0
                item['sentiment']=0
                yield item
        except:
            print('error')
        for t in response.selector.xpath("//a[@href]/@href").extract():
            if not t.startswith('http'):
                t="http://www.medkaoyan.net"+t
            if (self.bf.is_element_exist(t)==False):  # reduce a /
                yield Request(t,callback=self.parse_inPage)
            else:
                continue

    def parse_mainPage(self,response):
        sel=Selector(response)
        sites=sel.xpath("//a[@href]/@href").extract()
        while '' in sites:
            sites.remove('')
        while(1):
            for site in sites:
                if not site.startswith('http'):
                    urls = "http://www.medkaoyan.net"+site
                else:
                    urls=site
                if((self.bf.is_element_exist(urls.encode('utf-8'))==False) and (str(urls)!='http://www.medkaoyan.net/') and(str(urls)!='http://www.medkaoyan.net') and(str(urls).find('javascript')==-1)):
                    yield Request(urls,callback=self.parse_inPage)
                else:
                    continue
