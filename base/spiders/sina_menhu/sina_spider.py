# -*- coding: utf-8 -*-
import scrapy
import re
from base.items.sina_menhu.items import SinaScrapyItem

class DmozSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["sina.com.cn"]
    start_urls = [
        "http://www.sina.com.cn/"
        #"http://sports.sina.com.cn/g/pl/2017-10-16/doc-ifyfkqks4451477.shtml"
    ]

    def parse(self, response):
        r1 = '^http://.*.sina.*'
        r2 = '^http://.*.sina.*.shtml.*'
        r3 = '^http://.*video.sina.*'
        url = response.url
        try:
            if re.match(r2, url):
                #if re.match(r3, url):
                #with open('aaaa', 'ab') as f:
                 #f.write(url + '\n')
                print url
                print '\n'
                # print "aaaaaaa!!!!!!!@*#()@_______"
                # for sel in response:
                item = SinaScrapyItem()
                # item['name'] = sel.xpath("h1[@class='main-title']/text()").extract()[0].encode('utf-8')
                # name= item['name']
                item['url'] = url
                item['content'] = response.body
                item['source'] = "新浪网"
                item['source_url'] = "http://www.sina.com.cn/"
                # print name
                # with open('aaa', 'ab') as f:
                # f.write(response.url)
                # f.write('\n')
                yield item
        except:
            print('error')
        for url in response.selector.xpath("//a/@href").re(r1):
            if re.match(r3, url) == None:
                #with open('aaaaa', 'ab') as f:
                    #f.write(url+'\n')
                yield scrapy.Request(url=url, callback=self.parse)

    """ def parse(self, response):
           r1 = '^http://ent.sina.*'
           r2 = '^http://sports.sina.*'
           r3='^http://edu.sina.*'
           r4 = '^http://news.sina.*'
           r5='^http://tech.sina.*.'
           r6='^http://finance.sina.*'
           r='^http://[a-z.]*.sina.*'
           r0='^http://[a-z.]*.sina.*'
           url=response.url
           try:
               if re.match(r1,url):
                   for sel in response.xpath("//div[@class='main-content w1240']"):
                       item = SinaScrapyItem()
                       #item['name'] = sel.xpath("h1[@class='main-title']/text()").extract()[0].encode('utf-8')
                       #name= item['name']
                       item['url']=url
                       item['content']=response.body
                       item['source'] = "新浪网"
                       item['source_url'] = "http://www.sina.com.cn/"
                       #print name
                      # with open(name, 'wb') as f:
                           #f.write(response.body)
                       yield item
               if re.match(r2,url):
                   for sel in response.xpath("//article[@class='article-a']"):
                       item = SinaScrapyItem()
                       #item['name'] = sel.xpath("h1[@class='article-a__title']/text()").extract()[0].encode('utf-8')
                       item['url'] = url
                       item['content'] = response.body
                       item['source']="新浪网"
                       item['source_url']="http://www.sina.com.cn/"
                       #name = item['name']
                       #with open(name, 'wb') as f:
                           #f.write(response.body)
                       yield item
               if re.match(r3,url) or re.match(r5,url):
                   #print response.url
                   #print '\n'
                   #sel=response
                   for sel in response.xpath("//div[@class='main_content']"):
                       item = SinaScrapyItem()
                       #item['name'] = sel.xpath("h1[@id='main_title']/text()").extract()[0].encode('utf-8')
                       item['url'] = url
                       item['content'] = response.body
                       item['source'] = "新浪网"
                       item['source_url'] = "http://www.sina.com.cn/"
                       #name= item['name']
                       #print name
                       #with open(name, 'wb') as f:
                           #f.write(response.body)
                       yield item
               if re.match(r4,url) or re.match(r6,url):
                   for sel in response.xpath("//div[@class='page-header']"):
                       item = SinaScrapyItem()
                       #item['name'] = sel.xpath("h1[@id='artibodyTitle']/text()").extract()[0].encode('utf-8')
                       item['url'] = url
                       item['content'] = response.body
                       item['source'] = "新浪网"
                       item['source_url'] = "http://www.sina.com.cn/"
                       #name = item['name']
                       #with open(name, 'wb') as f:
                           #f.write(response.body)
                       yield item

               if re.match(r, url):
                   item = SinaScrapyItem()
                   with open('aaa', 'wb') as f:
                       f.write(response.body)
                   yield item


           except:
               print('error')
           for url in response.selector.xpath("//a/@href").re(r1+'|'+r2+'|'+r3+'|'+r4+'|'+r5+'|'+r6):

               yield scrapy.Request(url=url,callback = self.parse)
   """







