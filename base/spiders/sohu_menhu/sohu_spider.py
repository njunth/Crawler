# -*- coding: utf-8 -*-
import scrapy
import re
from base.items.sohu_menhu.items import SohuScrapyItem
from base.items.sohu_menhu.bloomfilter import BloomFilter
import sys
import datetime
class DmozSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["sohu.com"]
    start_urls = [
        "http://www.sohu.com"
    ]
    bf = BloomFilter(0.0001, 1000000)
    r1 = '.*.sohu.*'
    r2 = '^http://.*.sohu.*.shtml.*'
    r3 = '^http://.*.sohu.com/a/.*'
    r4 = '^http://.*.sohu.*.html.*'

    r5 = '.*tv.sohu.*'
    r6 = '^http://.*auto.sohu.*'
    r7 = '^http://.*upload.*'
    r8 = '^http://.*ad.sohu.*'
    r9='^http://.*mp.sohu.*'
    r10='^http://.*picture.*'
    r11='^http://.*/tag/.*'
    r12='^https://.*'
    def parse_inpage(self, response):

        url = response.url

        try:
            if re.match(self.r2, url)or re.match(self.r3, url):
            #if re.match(r2, url):
                #with open('aaaaa', 'ab') as f:
                    #f.write(url + '\n')
                #print url
                #print '\n'
                #print "aaaaaaa!!!!!!!@*#()@_______"
                #for sel in response:
                #with open('aaa', 'ab') as f:
                    #f.write(url + '\n')
                self.bf.insert_element(url)
                item = SohuScrapyItem()

                item['title'] = response.xpath("//head/title/text()").extract_first().encode('utf-8')
                # item['title'] = response.xpath("//h1/text()").extract_first().encode('utf-8')
                try:
                    item['content'] = response.xpath("//div[@id='article-container']//p/text() ").extract()
                except:
                    item['content'] = response.xpath("//div[@id='contentText']//p/text() ").extract()
                item['content'] = ''.join(item['content'])
                # name= item['name']
                item['url'] = url
                item['sentiment'] = 0
                item['attention'] = 0

                item['html'] = ''

                contentlist = response.xpath('//html').extract()
                for con in contentlist:
                    utfcontent = con.encode('utf-8')
                    item['html'] += utfcontent
                """
                try:
                    item['html'] = response.body.decode('gbk')
                except:
                    item['html'] = response.body
"""
                item['source'] = "搜狐网"
                item['source_url'] = "http://www.sohu.com/"

                time_item = []
                try:
                    time = response.xpath("//head/meta[@property='og:release_date']/@content").extract()[0]
                except:
                    time = response.xpath("//div[@class='time']/text()").extract()[0]

                #print time
                #print '\n'
                time_item.append(time[0:4])
                time_item += '_'
                time_item += time[5:7]
                time_item += '_'
                time_item += time[8:10]
                time_item += '_'
                time_item += time[11:13]
                time_item += '_'
                time_item += time[14:16]
                time_item = ''.join(time_item)
                item['time'] = time_item
                item['create_time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                #with open('aaaaa', 'ab') as f:
                    #f.write(response.url + '\n')

                yield item
        except:
            #print url
            #print '\n'
            #print(sys.exc_info())
            pass

    def parse(self, response):
        #with open('aaa', 'ab') as f:
         #f.write(response.url + '\n')
        for url in response.selector.xpath("//a/@href").re(self.r1):
            if not url.startswith('http:'):
                url = "http:"+ url
                #with open('aaaaaa', 'ab') as f:
                    #f.write(response.url+ '::'+ url + '\n')
            if re.match(self.r5,url) is None and re.match(self.r6,url) is None and re.match(self.r7,url) is None\
                    and re.match(self.r8,url) is None and re.match(self.r10,url) is None \
                    and re.match(self.r12, url) is None:
                if re.match(self.r2,url) or re.match(self.r3,url) or re.match(self.r4,url):
                    #with open('aa', 'ab') as f:
                        #f.write(response.url + '::' + url + '\n')
                    if (self.bf.is_element_exist(url) is False):
                        #with open('a', 'ab') as f:
                            #f.write(response.url + '::' + url + '\n')
                        yield scrapy.Request(url=url, callback=self.parse_inpage,priority=1)

                else:
                    #print url+'\n'
                        yield scrapy.Request(url=url, callback=self.parse, priority=0)