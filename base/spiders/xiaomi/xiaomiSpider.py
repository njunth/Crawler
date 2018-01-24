# coding=utf-8
import scrapy
from base.items.xiaomi.items import XiaomiItem
import re
import os
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from base.items.xiaomi.bloomfilter import BloomFilter
import string, random, time

class Xiaomispider(scrapy.Spider):
    name = "spider"

    allowed_domins = ["xiaomi.cn"]

    start_urls = {
        "http://bbs.xiaomi.cn/"
    }
    #bf = BloomFilter(0.0001,1000000)

    def start_requests(self):
        os.environ["all_proxy"] = "http://dailaoshi:D9xvyfrgPwqBx39u@bh21.84684.net:21026"
        while 1:
            yield scrapy.Request(url="http://bbs.xiaomi.cn/", callback=self.parse, dont_filter=True)


    def parse(self,response):
        # while 1:
        if 1==1:
            for url1 in response.selector.xpath("//a/@href").re(r'^http://bbs.xiaomi.cn/t-[0-9.]*'):
                #if (self.bf.is_element_exist(url1) == False):  # reduce a /
                yield scrapy.Request(url=url1, callback=self.parse_inpage, dont_filter=True)
            #else:
             #   continue

    def parse_inpage(self,response):
        sleep_time = random.random()
        # print sleep_time
        time.sleep( sleep_time )
        item = XiaomiItem()
        #content = response.selector.xpath("//div[@class='invitation_content']//p")#//text()").extract()
        #con_div = content.xpath('string(.)').extract()

        reply = response.selector.xpath("//div[@class='reply_txt']//p")#//text()").extract()
        reply_div = reply.xpath('string(.)').extract()

        if re.match('^http://bbs.xiaomi.cn/t-[0-9.]*', response.url) and len(reply_div)>0:
            # if re.match('^http://bbs.xiaomi.cn.*', response.url):
            item['source'] = "小米论坛"
            item['source_url'] = 'http://bbs.xiaomi.cn/'

            item['html'] = ''
            contentlist = response.xpath('//html').extract()
            # for con in contentlist:
            #     utfcontent = con.encode('utf-8')
            #     item['html'] += utfcontent


            item['url'] = response.url

            item['title'] = response.xpath("//h1//span[@class='name']/text()").extract()
            item['title'] = ''.join(item['title'])
            #if len(con_div) > 0:
            #item['content'] = con_div
            item['replies'] = reply_div#response.xpath("//p//text()").extract()
            #else:
            item['content'] = response.selector.xpath("//div[@class='invitation_content']//p//text()").extract()

            #item['replies'] = response.selector.xpath("//div[@class='reply_txt']//p//text()").extract()
            item['mainauth'] = response.xpath("//a[@class='user_name']/text()").extract_first()


            #item['n_click'] \
            n_click = response.xpath("//span[@class='f_r']//text()").extract_first()
            if n_click is None:
                item['n_click'] = 0
            else:
                nclick = ''.join(n_click)
                nc = nclick
                for c in string.punctuation:
                    nc = nc.replace(c, '')

                if nc is None:
                    item['n_click'] = 0
                else:
                    item['n_click'] = int(nc)

            #item['n_reply'] \
            n_reply = response.xpath("//span[@class='f_r']//text()").extract()[1]
            if n_reply is None:
                item['n_reply'] = 0
            else:
                nreply = ''.join(n_reply)
                nr = nreply
                for c in string.punctuation:
                    nr = nr.replace(c, '')

                if nr is None:
                    item['n_reply'] = 0
                else:
                    if nr is '':
                        item['n_reply'] = 0
                    else:
                        item['n_reply'] = int(nr)

            item['authid'] = response.xpath("//a[@class='auth_name']/text()").extract()
            item['time'] = response.xpath("//span[@class='time'][2]/text()").extract()
            item['maintime'] = response.xpath("//p[@class='txt']//span[@class='time']/text()").extract()

            item['sentiment'] = 0
            item['attention'] = 0

            yield item
            #self.bf.insert_element(response.url)



