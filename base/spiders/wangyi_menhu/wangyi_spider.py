# -*- coding: utf-8 -*-
import scrapy
import re
from base.items.wangyi_menhu.items import WangyiScrapyItem

class DmozSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["163.com"]
    start_urls = [
        "http://www.163.com/"
        #"http://sports.sina.com.cn/g/pl/2017-10-16/doc-ifyfkqks4451477.shtml"
    ]

    def parse(self, response):
        r1 = '^http://.*.163.*'
        r2='^http://.*.163.*.html'
        r3='^http://.*v.163.*'
        url = response.url
        try:
            if re.match(r2, url):
                print url
                print '\n'
                #print "aaaaaaa!!!!!!!@*#()@_______"
                #for sel in response:
                item = WangyiScrapyItem()
                # item['name'] = sel.xpath("h1[@class='main-title']/text()").extract()[0].encode('utf-8')
                # name= item['name']
                item['url'] = url
                item['content'] = response.body
                item['source'] = "网易网"
                item['source_url'] = "http://www.163.com/"
                # print name
                #with open('aaa', 'ab') as f:
                    #f.write(response.url)
                    #f.write('\n')
                yield item
        except:
            print('error')
        for url in response.selector.xpath("//a/@href").re(r1):
            if re.match(r3,url)==None:
                yield scrapy.Request(url=url, callback=self.parse)