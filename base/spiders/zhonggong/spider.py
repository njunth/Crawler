# coding=utf-8
import pytz
import scrapy
import os
from base.items.zhonggong.items import ZhonggongItem
from scrapy.http import Request
import datetime, random, time
# from base.items.zhonggong.BloomFilter import BloomFilter
import pyreBloom
from base.configs.settings import REDIS_HOST, REDIS_PORT


class spider( scrapy.Spider ):
    name = "spider"
    allowed_domains = ["www.kaoyan365.cn"]

    start_urls = ["http://www.kaoyan365.cn/"]
    tz = pytz.timezone( 'Asia/Shanghai' )

    def start_requests(self):
        self.bf = pyreBloom.pyreBloom( 'zhonggong', 100000, 0.0001, host=REDIS_HOST, port=REDIS_PORT )
        # os.environ["all_proxy"] = "http://dailaoshi:D9xvyfrgPwqBx39u@bh21.84684.net:21026"
        while 1:
            yield Request( "http://www.kaoyan365.cn/", callback=self.parse, dont_filter=True )

    def parse(self, response):
        # while 1:
        if 1 == 1:
            urls = response.xpath(
                "//div[@class='offcn_index_m1_center fl']//a[starts-with(@href,'http')]/@href   |  //div[@class='offcn_m2_right fr']//a[starts-with(@href,'http')]/@href   |   //div[@class='offcn_main3 offcn_mt20 layout']//*/a[starts-with(@href,'http')]/@href   |   //div[@class='offcn_main4 layout']//a[starts-with(@href,'http')]/@href   |   //div[@class='offcn_main7 offcn_mt20 layout']//a[starts-with(@href,'http')]/@href" ).extract()
            print urls
            for url in urls:
                if (self.bf.contains( url ) == False):
                    yield Request( url, callback=self.parse_inPage, dont_filter=True )
                else:
                    continue

    def parse_inPage(self, response):
        sleep_time = random.random()
        print sleep_time
        time.sleep( sleep_time )
        item = ZhonggongItem()
        item['title'] = ''
        item['source'] = "中公考研"
        item['source_url'] = "http://www.kaoyan365.cn/"
        item['url'] = response.url
        item['html'] = ''
        item['time'] = ''
        item['content'] = ''
        item['attention'] = 0
        item['sentiment'] = 0
        item['create_time'] = datetime.datetime.now(self.tz).strftime( '%Y_%m_%d_%H_%M_%S' )
        contentlist = response.xpath( "//html" ).extract()

        self.bf.extend( response.url )

        # for con in contentlist:
        # 	utfcontent = con.encode('utf-8')
        # 	item['html'] += utfcontent
        titlelist = response.xpath( '//title/text()' ).extract()

        for line in titlelist:
            title = line.encode( 'utf-8' )
            item['title'] += title

        timelist = response.xpath( "//div[@class='offcn_show_ly']/font[2]/text()" ).extract_first()
        if timelist is None:
            item['time'] = datetime.datetime.now(self.tz).strftime( '%Y_%m_%d_%H_%M_%S' )
        else:
            j = 0
            while (j <= 23):
                timelist = response.xpath( "//div[@class='offcn_show_ly']/font[2]/text()" ).extract_first()[j]
                if timelist == '2':
                    break
                j += 1
            i = 0
            while (i <= 18):
                timelist = response.xpath( "//div[@class='offcn_show_ly']/font[2]/text()" ).extract_first()[i + j]
                if timelist == '-' or timelist == ' ' or timelist == ':':
                    item['time'] += '_'
                else:
                    item['time'] += timelist.encode( 'utf-8' )
                i += 1

        contentlist = response.xpath( "//div[@class='offcn_show_cont_02']//text()" ).extract()
        for con in contentlist:
            content = con.encode( 'utf-8' )
            item['content'] += content
        yield item
