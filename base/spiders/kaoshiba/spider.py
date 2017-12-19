# -*- coding: UTF-8 -*-
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from base.items.kaoshiba.items import KaoshibaItem
from base.items.kaoshiba.bloomfliter import BloomFilter
from datetime import datetime
import os, random, time
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class KaoshibaSpider(Spider):
    name = 'spider'
    allowed_domains=["exam8.com"]


    def __init__(self, name=None, **kwargs):

        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

        self.bf=BloomFilter(0.0001,100000)
        self.mainpage="http://www.exam8.com/xueli/kaoyan/"


    def start_requests(self):
        yield Request(self.mainpage,callback=self.parse_mainPage, dont_filter=True)

    def parse_inPage(self,response):
        sleep_time = random.random()
        print sleep_time
        time.sleep( sleep_time )
        r1 = '.*html'
        url = response.url
        self.bf.insert_element(url)
        item =KaoshibaItem()
        content_div = response.selector.xpath('.//p')
        content1=content_div.xpath('string(.)').extract()
        try:
            if ((re.match(r1, url)and len(content_div)>0)) :
                item['source']="考试吧"
                item['source_url']='http://www.exam8.com/xueli/kaoyan/'
                item['url']=url
                item['html']=''
                i=0
                for t in content1:
                    tt = t.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
                    content1[i]=tt
                    i=i+1
                item['content'] = "".join(content1)
                item['title'] = response.selector.xpath("//title/text()").extract()[0]
                item['attention'] = 0
                time_str=response.selector.xpath("//div[@class='titiefu']")
                time_str1=time_str.xpath('string(.)').extract()[0]
                try:
                    s2=time_str1.replace('-','_').replace(' ','_').replace(':','_')
                    time_str3= re.findall(r'\w*([0-9]{4}_[0-9]+_[0-9]+_[0-9]+_[0-9]+_[0-9]+)\w*',s2)[0]
                    timelist=time_str3.split('_')
                    kk=0
                    for t in timelist:
                        if (len(t)==0):
                            timelist[kk]='00_'
                        elif(len(t)==1):
                            timelist[kk]='0'+t+'_'
                        else:
                            timelist[kk]=t+'_'
                        kk=kk+1
                    final_str=list(''.join(timelist))
                    final_str.pop()
                    item['time']=''.join(final_str)
                except:
                    item['time']='0000_00_00_00_00_00'
                item['sentiment']=0
                item['create_time']=str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
                yield item
        except:
            print('error')
        for t in response.selector.xpath("//a[@href]/@href").extract():
            if not t.startswith('http'):
                t="http://www.exam8.com/xueli/kaoyan"+t
            if (self.bf.is_element_exist(t)==False):
                yield Request(t,callback=self.parse_inPage, dont_filter=True)
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
                    urls = "http://www.exam8.com/xueli/kaoyan"+site
                else:
                    urls=site
                if((self.bf.is_element_exist(urls.encode('utf-8'))==False) and (str(urls)!='http://www.medkaoyan.net/') and(str(urls)!='http://www.medkaoyan.net') and(str(urls).find('javascript')==-1)):
                    yield Request(urls,callback=self.parse_inPage, dont_filter=True)
                else:
                    continue
