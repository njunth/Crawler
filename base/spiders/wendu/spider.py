# coding=utf-8
import pytz
import scrapy
import os
from base.items.wendu.items import WenduItem
from scrapy.http import Request
import datetime, random, time
# from base.items.wendu.BloomFilter import BloomFilter
import pyreBloom
from base.configs.settings import REDIS_HOST, REDIS_PORT


class wendu( scrapy.Spider ):
    name = "spider"
    allowed_domains = ["kaoyan.wendu.com"]

    start_urls = ["http://kaoyan.wendu.com"]
    tz = pytz.timezone( 'Asia/Shanghai' )

    def start_requests(self):
        self.bf = pyreBloom.pyreBloom( 'wendu', 100000, 0.0001, host=REDIS_HOST, port=REDIS_PORT )
        os.environ["all_proxy"] = "http://dailaoshi:D9xvyfrgPwqBx39u@bh21.84684.net:21026"
        while 1:
            yield Request( "http://kaoyan.wendu.com", callback=self.parse, dont_filter=True )

    def parse(self, response):
        # while 1:
        if 1 == 1:
            urls = response.xpath( "//*/a[starts-with(@href,'http')]/@href" ).extract()
            for url in urls:
                urlc = ''
                for urllist in url:
                    urll = urllist.encode( 'utf-8' )
                    urlc += urll
                if (self.bf.contains( urlc ) == False):
                    yield Request( url, callback=self.parse_inPage, dont_filter=True )
                else:
                    continue

    def parse_inPage(self, response):
        sleep_time = random.random()
        # print sleep_time
        time.sleep( sleep_time )
        item = WenduItem()
        item['title'] = ''
        item['source'] = "文都教育考研"
        item['source_url'] = "http://kaoyan.wendu.com"
        item['url'] = response.url
        item['html'] = ''
        item['time'] = ''
        item['content'] = ''
        item['attention'] = 0
        item['sentiment'] = 0
        item['create_time'] = datetime.datetime.now( self.tz ).strftime( '%Y_%m_%d_%H_%M_%S' )
        self.bf.extend( response.url )

        contentlist = response.xpath( '//html' ).extract()
        # for con in contentlist:
        # 	utfcontent = con.encode('utf-8')
        # 	item['html'] += utfcontent

        titlelist = response.xpath( '//title/text()' ).extract()
        for line in titlelist:
            title = line.encode( 'utf-8' )
            item['title'] += title

        timelist = response.xpath( "//span[@class='article-time']/text()" ).extract_first()
        if timelist is None:
            item['time'] = datetime.datetime.now( self.tz ).strftime( '%Y_%m_%d_%H_%M_%S' )
        else:
            i = 0
            while (i <= 15):
                timelist = response.xpath( "//span[@class='article-time']/text()" ).extract_first()[i]
                if timelist == '-' or timelist == ' ' or timelist == ':':
                    item['time'] += '_'
                else:
                    item['time'] += timelist
                i += 1
            item['time'] += '_00'

        contentlist = response.xpath( "//*/div[@id='content']//text()" ).extract()
        for con in contentlist:
            content = con.encode( 'utf-8' )
            item['content'] += content

        yield item
