# -*- coding: utf-8 -*-
import scrapy
import re
from base.items.sina_menhu.items import SinaScrapyItem
from base.items.sina_menhu.bloomfilter import BloomFilter
import sys
class DmozSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["sina.com.cn"]
    start_urls = [
        "http://www.sina.com.cn/"
        #"http://edu.sina.com.cn/"
    ]
    bf = BloomFilter(0.1, 10)
    def parse(self, response):
        r1 = '^http://.*.sina.*'
        r2 = '^http://.*.sina.*.shtml.*'
        r3 = '^http://.*video.sina.*'
        r4 = '^http://.*auto.sina.*'
        r_content1="//div[@id='artibody']//p/text()"
        r_time="span class=.*time.*>"
        url = response.url
        self.bf.insert_element(url)
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
                item['title'] = response.xpath("//head/title/text()").extract_first().encode('utf-8')
                #item['title'] = response.xpath("//h1/text()").extract_first().encode('utf-8')
                item['content']=response.xpath(r_content1).extract()
                # name= item['name']
                item['url'] = url
                item['sentiment'] = 0
                item['attention'] = 0
                try:
                    item['html'] = response.body.decode('gbk')
                except:
                    item['html'] = response.body
                item['source'] = "新浪网"
                item['source_url'] = "http://www.sina.com.cn/"
                #item['time']
                time_item=[]
                time= response.xpath("//head/meta[@property='article:published_time']/@content").extract()[0]
                #time1 = response.xpath("//head/meta[@property='article:published_time']//@content").extract()[1]
                time_item.append(time[0:4])
                time_item += '_'
                time_item += time[5:7]
                time_item += '_'
                time_item +=time[8:10]
                time_item += '_'
                time_item += time[11:13]
                time_item += '_'
                time_item += time[14:16]
                time_item = ''.join(time_item)
                item['time'] = time_item

                # with open('aaa', 'ab') as f:
                # f.write(response.url)
                # f.write('\n')
                yield item
        except:
            print(sys.exc_info())
        for url in response.selector.xpath("//a/@href").re(r1):
            if re.match(r3, url) == None and re.match(r4, url) == None:
                #with open('aaaaa', 'ab') as f:
                    #f.write(url+'\n')
                if (self.bf.is_element_exist(url) == False):
                    yield scrapy.Request(url=url, callback=self.parse)

