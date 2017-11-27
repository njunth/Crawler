# -*- coding: utf-8 -*-
import scrapy
import re
from base.items.wangyi_menhu.items import WangyiScrapyItem
from base.items.wangyi_menhu.bloomfilter import BloomFilter
import sys


class DmozSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["163.com"]
    start_urls = [
        "http://www.163.com/"
    ]

    def parse_inpage(self, response):
        # print response.url
        # print '\n'
        r1 = '^http://.*.163.*'
        r2 = '^http://.*.163.*.html'
        r3 = '^http://.*v.163.*'
        r4 = '^http://.*house.163.*'
        url = response.url
        self.bf.insert_element(url)
        item = WangyiScrapyItem()
        try:
            if re.match(r2, url):
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
                if item['content']:
                    # with open('aaaaa', 'ab') as f:
                    # f.write(url+'\n')
                    item['sentiment'] = 0
                    item['attention'] = 0
                    item['url'] = url
                    item['source'] = "网易网"
                    item['source_url'] = "http://www.163.com/"
                    try:
                        item['html'] = response.body.decode('gbk')
                    except:
                        item['html'] = response.body

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
                    # print name
                    # with open('aaa', 'ab') as f:
                    # f.write(response.url)
                    # f.write('\n')
                    yield item
        except:
            print url
            print(sys.exc_info())

    def parse(self, response):
        self.bf = BloomFilter(0.0001, 1000000)
        r1 = '^http://.*.163.*'
        r2 = '^http://.*.163.*.html'
        r3 = '^http://.*v.163.*'
        r4 = '^http://.*house.163.*'
        while 1:
            for url in response.selector.xpath("//a/@href").re(r1):
                # print url
                # print '\n'
                if re.match(r3, url) == None and re.match(r4, url) == None:
                    if (self.bf.is_element_exist(url) == False):
                        yield scrapy.Request(url=url, callback=self.parse_inpage)
                    else:
                        continue
                else:
                    continue
