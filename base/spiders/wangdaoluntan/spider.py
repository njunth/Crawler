# -*- coding: UTF-8 -*-
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from base.items.wangdaoluntan.items import WangdaoluntanItem
from base.items.wangdaoluntan.bloomfliter import BloomFilter
import os
import re

import sys

reload( sys )
sys.setdefaultencoding( 'utf8' )


class WangdaoluntanSpider(Spider):
    name = 'spider'
    allowed_domains=['cskaoyan.com']

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

    def start_requests(self):
        yield Request(self.mainpage,callback=self.parse_mainPage)

    def parse_inPage(self,response):
        r1 = 'http://www.cskaoyan.com/thread-[0-9]+-[0-9]+-[0-9]+.html'
        url = response.url
        self.bf.insert_element(url)
        item =WangdaoluntanItem()
        content_div = response.selector.xpath('//table[@cellspacing="0" and @cellpadding="0"]//tr//td[@class="t_f"]')
        content1=content_div.xpath('string(.)').extract()
        # print content1
      #  content_div2 = response.selector.xpath('//div[@align="left"]//font[@face]//font[@color]//font[@size]')
     #   content2=content_div2.xpath('string(.)').extract()
      #  print content2
        try:
            if (re.match(r1, url) and len(content1)>0):
                # print url
                print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
               # os.system("pause")
               #  print('!???????????')
                item['source']='wangdaoluntan'
                item['source_url']='http://www.cskaoyan.com/forum.php'
                item['url']=url
                item['html']=''
                # print item['url']
                #os.system("pause")
                item['content'] = content1
                item['title'] = response.selector.xpath("//title/text()").extract()[0]
                item['attention'] = 0
                text=str(response.body)
                time_str=response.selector.xpath("//em[@id]/text()").extract()[0]
                # print time_str
                item['time']=re.findall(r'(\w*[0-9]+-[0-9]+-[0-9]+)\w*',time_str)[0]
                # print item['time']
                click1 = response.selector.xpath("//span[@class='xi1']/text()").extract()
                if(len(click1)>0): item['n_click'] = int(click1[0])
                else:item['n_click']=0
                reply1 = response.selector.xpath("//span[@class='xi1']/text()").extract()
                if(len(click1)>1): item['n_reply'] = int(click1[1])
                else:item['n_reply']=0
                #os.system('pause')
                item['sentiment']=0
                #os.system("pause")
                yield item
            else:
                # print ("url not match")
                print url
                #os.system("pause")
        except:
            print('error')
            #os.system("pause")
        for t in response.selector.xpath("//a[@href]/@href").extract():
            if not t.startswith('http'):
                t="http://www.cskaoyan.com/"+t
            if (self.bf.is_element_exist(t)==False):  # reduce a /
                yield Request(t,callback=self.parse_inPage)
            else:
                continue

    def parse_mainPage(self,response):
        # print 1
        # print str(response.url)
       # rr = '^http://[a-z.]*.chinakaoyan.com/info/article/id.*'
        sel=Selector(response)
        sites=sel.xpath("//a[@href]/@href").extract()
        while (1):
            for site in sites:
                # print site
                if not site.startswith('http'):
                    urls = "http://www.cskaoyan.com/forum.php/"+site
                    # print urls
                    #os.system("pause")
                else:
                    urls=site
                # print urls
                if(self.bf.is_element_exist(urls)==False):
                    yield Request(urls,callback=self.parse_inPage)
                else:
                    continue
