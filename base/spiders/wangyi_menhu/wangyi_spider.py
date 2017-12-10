# -*- coding: utf-8 -*-
import scrapy
import re
from base.items.wangyi_menhu.items import WangyiScrapyItem
from base.items.wangyi_menhu.bloomfilter import BloomFilter
import sys

import datetime

class DmozSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["163.com"]
    start_urls = [
        "http://www.163.com/"
    ]

    r1 = '^http://.*.163.*'
    r2 = '^http://.*.163.*.html'
    r3 = '^http://.*v.163.*'
    r4 = '^http://.*house.163.*'
    r5 = '^http://.*.163.*.shtml'
    bf = BloomFilter(0.0001, 1000000)
    def parse_inpage(self, response):
        # print response.url
        # print '\n'

        url = response.url
        self.bf.insert_element(url)
        item = WangyiScrapyItem()
        try:
            if re.match(self.r2, url):
                # with open('aaaaa', 'ab') as f:
                # f.write(url+'\n')
                # print url
                # print '\n'
                # print "aaaaaaa!!!!!!!@*#()@_______"
                # for sel in response:
                item['title'] = response.xpath("//head/title/text()").extract()[0]
                # name= item['name']
                item['content'] = response.xpath(
                    "//div[@class='post_content_main']//div[@id='endText']//p/text()").extract()
                item['content'] = ''.join(item['content'])
                if item['content']:
                    # with open('aaaaa', 'ab') as f:
                    # f.write(url+'\n')
                    item['sentiment'] = 0
                    item['attention'] = 0
                    item['url'] = url
                    item['source'] = "网易网"
                    item['source_url'] = "http://www.163.com/"
                    """
                    try:
                        item['html'] = response.body.decode('gbk')
                    except:
                        item['html'] = response.body
"""
                    item['html'] = ''
                    contentlist = response.xpath('//html').extract()
                    for con in contentlist:
                        utfcontent = con.encode('utf-8')
                        item['html'] += utfcontent

                    time_item = []
                    time = response.xpath("//*[@class='post_time_source']/text()").extract()
                    # time1 = response.xpath("//head/meta[@property='article:published_time']//@content").extract()[1]
                    time = ''.join(time)
                    time = re.sub(r'\s', '', time)
                    # print time
                    # print "\naaaaaaaaaaa\n"
                    time_item.append(time[0:4])
                    time_item += '_'

                    time_item += time[5:7]
                    time_item += '_'
                    time_item += time[8:10]
                    time_item += '_'
                    time_item += time[10:12]
                    time_item += '_'
                    time_item += time[13:15]

                    time_item = ''.join(time_item)
                    item['time'] = time_item
                    item['create_time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                    # print name
                    # with open('aaa', 'ab') as f:
                    # f.write(response.url)
                    # f.write('\n')
                    yield item
        except:
            #print url
            #print(sys.exc_info())
            pass

    def parse(self, response):
        """
        with open('aaaa', 'ab') as f:
            f.write(response.url)
            f.write('\n')
            """
        for url in response.selector.xpath("//a/@href").re(self.r1):
            if re.match(self.r2, url) is None and re.match(self.r3, url) is None and re.match(self.r4, url) is None \
                    and re.match(self.r4, url) is None and re.match(self.r5, url) is None:
                yield scrapy.Request(url=url, callback=self.parse, priority=0)

            else:
                if re.match(self.r3, url) == None and re.match(self.r4, url) == None:
                    if (self.bf.is_element_exist(url) == False):
                        yield scrapy.Request(url=url, callback=self.parse_inpage, priority=1)
