# coding=utf-8
import pytz
import scrapy
import os
from base.items.zhuoyue.items import ZhuoyueItem
from scrapy.http import Request
import datetime, random, time
# from base.items.zhuoyue.BloomFilter import BloomFilter
# from base.items.Bloomfilter import BloomFilter
import pyreBloom
from base.configs.settings import REDIS_HOST, REDIS_PORT


class spider( scrapy.Spider ):
    name = "spider"
    allowed_domains = ["www.zhuoyuekaoyan.com"]

    start_urls = ["http://www.zhuoyuekaoyan.com"]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    tz = pytz.timezone( 'Asia/Shanghai' )

    def start_requests(self):
        self.bf = pyreBloom.pyreBloom( 'zhuoyue', 100000, 0.0001, host=REDIS_HOST, port=REDIS_PORT )
        # os.environ["all_proxy"] = "http://dailaoshi:D9xvyfrgPwqBx39u@bh21.84684.net:21026"
        while 1:
            yield Request( "http://www.zhuoyuekaoyan.com", callback=self.parse, dont_filter=True )

    def parse(self, response):
        # while 1:
        if 1 == 1:
            urls = response.xpath( "//*/a/@href" ).extract()
            for url in urls:
                urlc = 'http://www.zhuoyuekaoyan.com'
                if not url.startswith( 'http' ):
                    for urllist in url:
                        urll = urllist.encode( 'utf-8' )
                        urlc += urll
                # print urlc
                if (self.bf.contains( urlc ) == False):
                    yield Request( urlc, callback=self.parse_inPage, dont_filter=True )
                else:
                    continue

    def parse_inPage(self, response):
        sleep_time = random.random()
        # print sleep_time
        time.sleep( sleep_time )
        item = ZhuoyueItem()
        item['title'] = ''
        item['source'] = "卓越考研"
        item['source_url'] = "http://www.zhuoyuekaoyan.com"
        item['url'] = response.url
        print item['url']
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

        timelist = response.xpath( "//div[@class='detail-subtitle']/span/text()" ).extract_first()
        if timelist is None:
            item['time'] = datetime.datetime.now(self.tz).strftime( '%Y_%m_%d_%H_%M_%S' )
        else:
            i = 0
            while (i <= 15):
                timelist = response.xpath( "//div[@class='detail-subtitle']/span/text()" ).extract_first()[i + 5]
                if timelist == '-' or timelist == ' ' or timelist == ':':
                    item['time'] += '_'
                else:
                    item['time'] += timelist.encode( 'utf-8' )
                i += 1
            item['time'] += '_00'

        contentlist = response.xpath( "//div[@class='detail-main']//text()" ).extract()
        for con in contentlist:
            content = con.encode( 'utf-8' )
            item['content'] += content
        yield item

        urls = response.xpath( "//*/a/@href" ).extract()
        for url in urls:
            urlc = 'http://www.zhuoyuekaoyan.com'
            for urllist in url:
                urll = urllist.encode( 'utf-8' )
                urlc += urll
            if (self.bf.contains( urlc ) == False):
                yield Request( urlc, callback=self.parse_inPage, dont_filter=True )

            else:
                continue
