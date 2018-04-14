# coding=utf-8
import pytz
import scrapy
import os
from base.items.xindongfang.items import XinItem
from scrapy.http import Request
import datetime, random, time
# from base.items.xindongfang.BloomFilter import BloomFilter
import pyreBloom
from base.configs.settings import REDIS_HOST, REDIS_PORT


class spider( scrapy.Spider ):
    name = "spider"
    allowed_domains = ["kaoyan.koolearn.com"]

    start_urls = ["http://kaoyan.koolearn.com"]
    tz = pytz.timezone( 'Asia/Shanghai' )

    def start_requests(self):
        self.bf = pyreBloom.pyreBloom( 'xindongfang', 100000, 0.0001, host=REDIS_HOST, port=REDIS_PORT )
        os.environ["all_proxy"] = "http://dailaoshi:D9xvyfrgPwqBx39u@bh21.84684.net:21026"
        while 1:
            yield Request( "http://kaoyan.koolearn.com", callback=self.parse, dont_filter=True )

    def parse(self, response):
        # while 1:
        if 1 == 1:
            urls = response.xpath( "//li/a/@href|//div/a/@href|//td/a/@href" ).extract()
            for url in urls:
                if (self.bf.contains( url ) == False):
                    yield Request( url, callback=self.parse_inPage, dont_filter=True )
                else:
                    continue

    def parse_inPage(self, response):
        sleep_time = random.random()
        # print sleep_time
        time.sleep( sleep_time )
        item = XinItem()
        item['title'] = ''
        item['source'] = "新东方"
        item['source_url'] = "http://kaoyan.koolearn.com"
        item['url'] = response.url
        item['html'] = ''
        item['time'] = ''
        item['content'] = ''
        item['attention'] = 0
        item['sentiment'] = 0
        item['create_time'] = datetime.datetime.now(self.tz).strftime( '%Y_%m_%d_%H_%M_%S' )
        contentlist = response.xpath( '//html' ).extract()

        self.bf.extend( response.url )

        # for con in contentlist:
        # 	utfcontent=con.encode('utf-8')
        # 	item['html']+=utfcontent
        titlelist = response.xpath( '//title/text()' ).extract()

        for line in titlelist:
            title = line.encode( 'utf-8' )
            item['title'] += title

        timelist = response.xpath( "//i[@class='s_tit_i1']/text()" ).extract_first()
        if timelist is None:
            item['time'] = datetime.datetime.now(self.tz).strftime( '%Y_%m_%d_%H_%M_%S' )
        else:
            i = 0
            while (i <= 18):
                if i != 4 and i != 7 and i != 10 and i != 13 and i != 16:
                    timelist = response.xpath( "//i[@class='s_tit_i1']/text()" ).extract_first()[i]
                    item['time'] += timelist
                else:
                    item['time'] += '_'
                i += 1

        contentlist = response.xpath( "//div[@class='mt40']//text()" ).extract()
        for con in contentlist:
            content = con.encode( 'utf-8' )
            item['content'] += content

        yield item
