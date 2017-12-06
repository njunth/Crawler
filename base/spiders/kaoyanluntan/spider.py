#encoding=utf-8
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from base.items.kaoyanluntan.items import KaoyanluntanItem
from base.items.kaoyanluntan.bloomfliter import BloomFilter
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class KaoyanluntanSpider(Spider):
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

        self.mainpage="http://bbs.kaoyan.com/"


    def start_requests(self):
        yield Request(self.mainpage,callback=self.parse_mainPage)

    def parse_inPage(self,response):
        r1 = 'http://bbs.kaoyan.com/t[0-9]*p1'
        url = response.url
        item =KaoyanluntanItem()
        content_div = response.selector.xpath('//table[@cellspacing="0" and @cellpadding="0"]//tr//td[@class="t_f"]')
        content1=content_div.xpath('string(.)').extract()

        try:
            if (re.match(r1, url) and len(content_div)>0):
                print url
                item['source']='kaoyanluntan'
                item['source_url']='http://bbs.kaoyan.com/'
                item['url']=url
                item['html']=response.body
                item['content'] = content1
                item['title'] = response.selector.xpath("//title/text()").extract()[0]
                item['attention']=0
                time_str=response.selector.xpath("//em[@id]/text()").extract()
                item['time']=time_str
                item['n_click'] = int(response.selector.xpath("//span[@class='xi1']/text()").extract()[0])
                item['n_reply'] = int(response.selector.xpath("//span[@class='xi1']/text()").extract()[1])
                item['sentiment']=0
                authid_str=response.selector.xpath("//div[@class='authi']//a[@class='xw1']/text()").extract()
                item['authid']=authid_str
                yield item
        except:
            print('error')
        for t in response.selector.xpath("//a[@href]/@href").extract():
            if not t.startswith('http'):
                t="http://bbs.kaoyan.com"+t
            yield Request(t,callback=self.parse_inPage)

    def parse_mainPage(self,response):
        sel=Selector(response)
        sites=sel.xpath("//a[@href]/@href").extract()
        while(1):
            for site in sites:
                if not site.startswith('http'):
                    urls = "http://bbs.kaoyan.com"+site
                else:
                    urls=site
                yield Request(urls,callback=self.parse_inPage)

