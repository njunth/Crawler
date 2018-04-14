# coding=utf-8
import pytz
import scrapy
from base.items.sina.items import SinaItem
import re
import os
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from base.items.sina.bloomfilter import BloomFilter
import string
import datetime, random, time

class Sinaspider(scrapy.Spider):
    name = "spider"

    allowed_domins = ["sina.com.cn"]

    start_urls = {
        "http://people.sina.com.cn/"
        # "http://club.eladies.sina.com.cn/thread-6490945-1-1.html"
        # "http://club.eladies.sina.com.cn/thread-6596256-1-1.html"
    }
    #bf = BloomFilter(0.0001,1000000)
    tz = pytz.timezone( 'Asia/Shanghai' )

    def start_requests(self):
        os.environ["all_proxy"] = "http://dailaoshi:D9xvyfrgPwqBx39u@bh21.84684.net:21026"
        while 1:
            yield scrapy.Request(url="http://people.sina.com.cn/forum/", callback=self.parse, dont_filter=True)


    def parse(self, response):
        # while 1:
        if 1==1:
            # print response.selector.xpath("//a/@href")
            for url1 in response.selector.xpath("//a/@href").re(r'^http://club.[a-z.]*.sina.*'):
                #if (self.bf.is_element_exist(url1) == False):  # reduce a /
                print url1
                yield scrapy.Request(url=url1, callback=self.parse_inpage, dont_filter=True)
                # sleep_time = random.random()
                # # print sleep_time
                # time.sleep( sleep_time )
                #else:
                    #continue
            #for url1 in response.selector.xpath("//a/@href").re(r'^http://club.[a-z.]*.sina.*'):
             #   yield scrapy.Request(url=url1, callback=self.parse)


    def parse_inpage(self,response):
        item = SinaItem()
        reply = response.selector.xpath("//div[@class='cont f14']")#//text()")  # .extract()
        reply1 = reply.xpath('string(.)').extract()

        #if reply is not None:
         #   reply1 = reply[0].xpath('string(.)').extract()
        #else:
         #   reply1 = None

        #author = response.selector.xpath("//div[@class='myInfo_up']/a")#/text()").extract()
        #if author is not None:
        #author1 = author.xpath('string(.)').extract()
        #else:
         #   author1 = None
        print response.url

        #if re.match('^http://club.[a-z.]*.sina.*.html', response.url):
        if re.match('^http://club.[a-z.]*.sina.com.cn/thread-[0-9]+-[0-9]+-[0-9]+.html', response.url) and len(reply1)>0:
            item['source'] = "新浪论坛"
            item['source_url'] = 'http://people.sina.com.cn/'

            item['html'] = ''
            contentlist = response.xpath('//html').extract()
            # for con in contentlist:
            #     utfcontent = con.encode('utf-8')
            #     item['html'] += utfcontent
            titlelist = response.xpath('//title/text()').extract()

            """try:
                item['html'] = response.body.decode('gbk')
            except:
                item['html'] = response.body"""
            item['url'] = response.url
            print item['url']

            #item['title'] = response.xpath("//head/title/text()").extract()[0].encode('utf-8')
            t = response.xpath("//head/title/text()").extract()#[0].encode('utf-8')
            title = ''.join(t)
            title1 = title.encode('utf-8')
            item['title'] = title1

            try:
                #item['content']  = response.xpath("//div[@class='maincont']//p//text()").extract()
                item['content'] = response.xpath("//div[@class='cont f14']//text()").extract()
            except:
                item['content'] = response.xpath("//div[@class='postmessage defaultpost']//text()").extract()

            #item['replies'] =
            #reply = response.selector.xpath("//div[@class='cont f14']//text()")#.extract()
            #item['replies'] = response.xpath("//div[@class='cont f14']//text()").extract()
            #item['replies'] = reply.xpath('string(.)').extract()#response.xpath("//div[@class='cont f14']//text()").extract()#reply.xpath('string(.)').extract()
            item['replies'] = reply1


            #item['replies'] = ''.join(item['replies'])
            #item['content'] = response.xpath("//tbody//p//font/text()").extract()

            #item['content'] = response.xpath("//div[@class='mybbs_cont']/text()").extract()
            #try:
             #   item['content'] = response.xpath("//div[@class='mainbox']//p//text()").extract()
            #except:
             #   item['content'] = response.xpath("//td[@class='postcontent']//text()").extract()


            #item['content'] = ''.join(item['content'])
            try:
                item['authid'] = response.xpath("//div[@class='myInfo_up']//a[@class='f14']/text()").extract()#不要first获得全部
            except:
                item['authid'] = response.xpath("//td[@class='postauthor']/text()").extract()

            #item['authid'] = author1#''.join(item['authid'])


            try:
                item['testtime'] = response.xpath("//div[@class='myInfo_up']//font/text()").extract()
            except:
                item['testtime'] = response.xpath("//td[@class='postauthor']/text()").extract()
                #item['testtime'] = item['testtime'][3]




            n_click = response.xpath("//div[@class='maincont']//tbody//span/font/text()").extract_first()
            #item['n_click'] = n_click
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


            #n_reply = response.xpath("//div[@class='maincont']//tbody//span/font/text()").extract()[1]
            n_reply = response.xpath("//div[@class='maincont']//span/font[2]/text()").extract()

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



            time_item = []
            time = response.xpath("//div[@class='maincont']//tbody//font/text()").extract_first()
            if time is None:
                item['time'] = datetime.datetime.now(self.tz).strftime('%Y_%m_%d_%H_%M_%S')
            else:
                time_item.append(time[4:8])
                time_item.append('_')
                time_item.append(time[9:11])
                time_item.append('_')
                time_item.append(time[12:14])
                time_item.append('_')
                time_item.append(time[15:17])
                time_item.append('_')
                time_item.append(time[18:20])

                timeitem = ''.join(time_item)
                item['time'] = timeitem

            item['sentiment'] = 0
            item['attention'] = 0
            item['create_time'] = datetime.datetime.now(self.tz).strftime( '%Y_%m_%d_%H_%M_%S' )
            yield item
            #self.bf.insert_element(response.url)

