# -*-coding:utf-8-*-
import scrapy
from scrapy.spiders import Spider
import pyreBloom
from base.configs.settings import REDIS_HOST, REDIS_PORT
from base.configs.google.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_TABLE, MYSQL_USER, MYSQL_PASSWORD, KEYWORD_INDEX, SPIDER_COUNTS
from base.items.google.items import ScrapyGoogleItem
import sys
import time
import pytz
import redis
import MySQLdb
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')


class GoogleSpider(Spider):
    name = 'spider'
    def __init__(self):
        self.tz = pytz.timezone( 'Asia/Shanghai' )
        # r = redis.Redis( host=REDIS_HOST, port=REDIS_PORT)#, db = 0)
        self.r = redis.StrictRedis( host=REDIS_HOST, port=REDIS_PORT )
        if self.r.exists("googlesousuo.0"):
            print "googlesousuo.0 exist"
            self.bf = pyreBloom.pyreBloom( 'googlesousuo', 100000, 0.0001, host=REDIS_HOST, port=REDIS_PORT )
            print self.r.ttl( 'googlesousuo.0' )
        else:
            print "creat googlesousuo.0"
            # r.set('baidusousuo.0','')
            self.bf = pyreBloom.pyreBloom( "googlesousuo", 100000, 0.0001, host=REDIS_HOST, port=REDIS_PORT )
            tests = "Hello google!"
            self.bf.extend( tests )
            print self.r.expire( 'googlesousuo.0', 60*60*24*3 )
            time.sleep(3)

            # print self.bf.contains( 'hello' )
            # # True
            # print self.bf.contains( ['hello', 'whats', 'new', 'with', 'you'] )
            # # ['hello', 'you']
            # print 'hello' in self.bf
            # print self.r.get('baidusousuo')
            print self.r.ttl( 'googlesousuo.0' )

    def start_requests(self):
        headers = {
            'Host': 'www.google.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            # 'Accept-Encoding':'gzip, deflate, br'
        }
        # keywords = ['你好']
        while 1:
            db = MySQLdb.connect( host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                                  db=MYSQL_DATABASE, charset='utf8' )
            cursor = db.cursor()
            sql = "SELECT DISTINCT name FROM keyword_t"
            cursor.execute( sql )
            keywords = cursor.fetchall()
            url_p1 = 'https://www.google.com/search?q='
            url_p2 = '&tbs=qdr:w,sbd:1&hl=zh&start='
            for i in range( 20, 0, -1 ):
                # print i
                index = 0
                for keyword in keywords[::-1]:
                    # print keyword[0]
                    if index % SPIDER_COUNTS == KEYWORD_INDEX:
                        url = url_p1 + keyword[0] + url_p2 + str( i*10 )
                        time.sleep( 1 )
                        print index, keyword[0], url
                        yield scrapy.Request( url=url, headers=headers, dont_filter=True, callback=self.parse,
                                              meta={'keyword': keyword[0]} )
                    index += 1

            # for keyword in keywords:
            #     for i in range(20):
            #         url = url_p1 + keyword + url_p2 + str(i*10)
            #         time.sleep(1)
            #         yield scrapy.Request(url=url,headers=headers,dont_filter=True,callback=self.parse,meta={'keyword':keyword})

    def parse(self, response):
        # print response.text
        keyword = response.meta['keyword']
        results = response.xpath( '//div[@class="rc"]' )
        time = datetime.datetime.now(self.tz)
        for res in results:
            url = res.xpath( './/h3[contains(@class,"r")]/a/@href' ).extract_first()
            # print keyword, url
            bfdata = str( keyword ) + str( url )
            print self.r.ttl( 'googlesousuo.0' ),
            if self.r.ttl( 'googlesousuo.0' ) < 0:
                print self.r.exists( 'googlesousuo.0' ),
                self.bf = pyreBloom.pyreBloom( "googlesousuo", 100000, 0.0001, host=REDIS_HOST, port=REDIS_PORT )
                # tests = "Hello baidu!"
                # self.bf.extend( tests )
                print self.r.expire( 'googlesousuo.0', 60 * 60 * 24 * 3 )
            if (self.bf.contains( str( bfdata ) ) == False):
                self.bf.extend( str( bfdata ) )
                item = ScrapyGoogleItem()
                item['url'] = url
                item['title'] = res.xpath( './/h3[contains(@class,"r")]/a' ).xpath( 'string(.)' ).extract_first()
                print item['title']
                timestr = res.xpath( './/span[contains(@class,"f")]' ).xpath( 'string(.)' ).extract_first()
                if timestr == None:
                    timestr = res.xpath( './/div[contains(@class,"slp f")]' ).xpath( 'string(.)' ).extract_first()
                if timestr == None:
                    item['time'] = time.strftime( '%Y_%m_%d_%H_%M_%S' )
                else:
                    timestr = timestr.split( ' ' )
                    time_type = timestr[1]
                    time_num = int( timestr[0] )
                    # print time_type
                    if time_type == '秒钟前':
                        delta = datetime.timedelta( seconds=time_num )
                        new_time = time - delta
                        item['time'] = new_time.strftime( '%Y_%m_%d_%H_%M_%S' )
                        # print time_num
                    elif time_type == '分钟前':
                        delta = datetime.timedelta( minutes=time_num )
                        new_time = time - delta
                        item['time'] = new_time.strftime( '%Y_%m_%d_%H_%M_%S' )
                        # print time_num
                    elif time_type == '小时前':
                        delta = datetime.timedelta( hours=time_num )
                        new_time = time - delta
                        item['time'] = new_time.strftime( '%Y_%m_%d_%H_%M_%S' )
                        # print time_num
                    elif time_type == '天前':
                        delta = datetime.timedelta( days=time_num )
                        new_time = time - delta
                        item['time'] = new_time.strftime( '%Y_%m_%d_%H_%M_%S' )
                        # print time_num
                abstract = res.xpath( './/span[contains(@class,"st")]' ).xpath( 'string(.)' ).extract_first()
                s = abstract.find( '-' )
                if s > 0:
                    abstract = abstract[s + 2:]
                # if abstract == None:
                #     # print res.extract()
                #     abstract = res.xpath('.//div[@class="c-span18 c-span-last"]/font/p').xpath('string(.)').extract()
                #     abstract = ' '.join(abstract)
                #     # print abstract
                # print abstract
                item['abstract'] = abstract
                item['keyword'] = unicode( keyword )
                item['create_time'] = time.strftime( '%Y_%m_%d_%H_%M_%S' )
                yield item