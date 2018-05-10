# coding=utf-8
import pytz
import scrapy
import os
from base.items.kaidi.items import KaidiItem
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
# from base.items.kaidi.bloomfilter import BloomFilter
import datetime, random, time

class KdSpider(scrapy.Spider):
    name = "spider"

    allowed_domins = ["kdnet.net"]

    start_urls = {
        "http://club.kdnet.net/index.asp"
    }
    # bf = pyreBloom.pyreBloom( 'kaicheng', 100000, 0.0001, host=REDIS_HOST, port=REDIS_PORT )
    tz = pytz.timezone( 'Asia/Shanghai' )

    def start_requests(self):
        # os.environ["all_proxy"] = "http://dailaoshi:D9xvyfrgPwqBx39u@bh21.84684.net:21026"
        while 1:
            yield scrapy.Request( url="http://club.kdnet.net/index.asp", callback=self.parse, dont_filter=True )


    def parse(self,response):
        # while 1:
        # print response.selector.xpath("//a/@href")
        # print response.selector.xpath("//a/@href").re(r'^//club.kdnet.net.*.id=[0-9.]*')
        if 1==1:
            # print len(response.selector.xpath("//a/@href").re(r'^//club.kdnet.net.*.id=[0-9.]*'))
            for url1 in response.selector.xpath("//a/@href").re(r'^//club.kdnet.net.*.id=[0-9.]*'):
                # yield scrapy.Request(url=url1, callback=self.parse)
                print url1
            #if (self.bf.is_element_exist(url1) == False):  # reduce a /
                yield scrapy.Request(url="http:"+url1, callback=self.parse_inpage, dont_filter=True)
            #else:
             #   continue


    def parse_inpage(self,response):
        sleep_time = random.random()
        print sleep_time
        time.sleep( sleep_time )
        item = KaidiItem()
        content = response.selector.xpath("//div[@class='replycont-text']")#//text()").extract()
        con_div = content.xpath('string(.)').extract()

        if re.match('^http://club.kdnet.net.*.id=[0-9.]*', response.url) and len(con_div) > 0:
            item['source'] = "凯迪社区"
            item['source_url'] = 'http://club.kdnet.net/index.asp'

            item['html'] = ''
            contentlist = response.xpath('//html').extract()
            # for con in contentlist:
            #     utfcontent = con.encode('utf-8')
            #     item['html'] += utfcontent

            item['url'] = response.url
            print item['url']

            item['attention'] = 0
            item['sentiment'] = 0
            item['create_time'] = datetime.datetime.now(self.tz).strftime('%Y_%m_%d_%H_%M_%S')

            item['content'] = response.selector.xpath("//div[@class='posts-cont']//text()").extract()
            item['content'] = ''.join(item['content'])
            #item['replies'] = response.selector.xpath("//div[@class='replycont-text']//text()").extract()
            item['replies'] = con_div
            item['authid'] = response.selector.xpath("//span[@class='name c-main']/a//text()").extract()

            """time = response.xpath("//div[@class='posted-info c-sub']//text()").extract()
            i = 0
            for t in time:
                temp = re.findall(r'(\w*[0-9]+])\w*', t)
                if temp is not None:
                    item['time'][i] = t
                    i = i + 1"""
            item['time'] = response.xpath("//div[@class='posted-info c-sub']//text()").extract()


            item['n_click'] = response.xpath("//span[@class='f10px fB c-alarm']//text()").extract_first()
            item['n_click'] = ''.join(item['n_click'])
            item['n_click'] = int(item['n_click'])

            item['n_reply'] = response.xpath("//span[@class='f10px fB c-alarm']//text()").extract()[1]
            item['n_reply'] = ''.join(item['n_reply'])
            item['n_reply'] = int(item['n_reply'])

            item['title'] = response.xpath("//div[@class='posts-title']//text()").extract()
            item['title'] = ''.join(item['title'])
            item['create_time'] = datetime.datetime.now(self.tz).strftime('%Y_%m_%d_%H_%M_%S')

            item['testtime'] = response.xpath("//div[@class='posts-posted']//text()").extract()
            k = 0
            for s in item['testtime']:
                temp = re.findall(r'(\w*[0-9]+/[0-9]+/[0-9]+ [0-9]+:[0-9]+:[0-9]+)\w*', s)
                if temp is not None and temp is not '':
                    item['testtime'][k] = temp
                    item['testtime'][k] = ''.join(item['testtime'][k])
                    k = k + 1
            #n = 0
            for t in item['testtime']:
                tem = []
                if t is not None and t is not '':
                    tempp = re.findall(r'(\w*[0-9]+)\w*', t)
                    tem.append(tempp[0])
                    tem.append('_')
                    if len(tempp[1]) is 1:
                        tem.append('0')
                        tem.append(tempp[1])
                    else:
                        tem.append(tempp[1])
                    tem.append('_')

                    if len(tempp[2]) is 1:
                        tem.append('0')
                        tem.append(tempp[2])
                    else:
                        tem.append(tempp[2])
                    tem.append('_')
                    tem.append(tempp[3])
                    tem.append('_')
                    tem.append(tempp[4])
                    tem.append('_')
                    tem.append(tempp[5])
                    # tem.append('_')
                    tem = ''.join(tem)
                    item['testtime'] = tem
                    #n = n + 1

            yield item
            #self.bf.insert_element(response.url)






