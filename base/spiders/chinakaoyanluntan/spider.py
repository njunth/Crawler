# -*- coding: UTF-8 -*-
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from base.items.chinakaoyanluntan.items import ChinakaoyanluntanItem
from base.items.chinakaoyanluntan.bloomfliter import BloomFilter
import os
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

        self.bf=BloomFilter(0.0001,100000)
        self.mainpage="http://www.chinakaoyan.com/club/clubHome/clubId/214.shtml"


    def start_requests(self):
        yield Request(self.mainpage,callback=self.parse_mainPage)

    def parse_inPage(self,response):
        r1 = '.*/club/topicShow/clubId/[0-9]*/tid.*'
        url = response.url
        self.bf.insert_element(url)
        item =ChinakaoyanluntanItem()
        content_div = response.selector.xpath('//div[@class="yq11n"]/text()').extract()
        try:
            if (re.match(r1, url) and len(content_div)>0):
                print url
                #print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
               # os.system("pause")
                #print('!???????????')
                item['source']='chinakaoyanluntan'
                item['source_url']='http://www.chinakaoyan.com/'
                item['url']=url
                item['html']=response.body
                click_reply_str=response.selector.xpath("//h6/text()").extract()[0]
                ccrr = re.findall(r'(\w*[0-9]+)\w*',click_reply_str)
                if(len(ccrr)>0):
                    item['n_click']=int(ccrr[0])
                else:
                    item['n_click']=0
                print item['n_click']
                if(len(ccrr)>1):
                    item['n_reply']=int(ccrr[1])
                else:
                    item['n_reply']=0
                print item['n_reply']
                print item['url']
                #os.system("pause")
                item['content'] = content_div
                item['title'] = response.selector.xpath("//title/text()").extract()[0]
                item['attention'] = 0
                text=str(response.body)
                item['time'] =re.search(r'\d+-\d+-\d+',text).group(0)
                print item['time']
                #os.system('pause')
                item['sentiment']=0
                #os.system("pause")
                yield item
        except:
            print('error')
            #os.system("pause")
        for t in response.selector.xpath("//a[@href]/@href").extract():
            if not t.startswith('http'):
                t="http://www.chinakaoyan.com"+t
            if (self.bf.is_element_exist(t)==False):  # reduce a /
                yield Request(t,callback=self.parse_inPage)
            else:
                continue

    def parse_mainPage(self,response):
        print str(response.url)
       # rr = '^http://[a-z.]*.chinakaoyan.com/info/article/id.*'
        sel=Selector(response)
        sites=sel.xpath("//a[@href]/@href").extract()
        while(1):
            for site in sites:
                if not site.startswith('http'):
                    urls = "http://www.chinakaoyan.com"+site
                else:
                    urls=site
                print urls
                if(self.bf.is_element_exist(urls)==False):
                    yield Request(urls,callback=self.parse_inPage)
                else:
                    continue