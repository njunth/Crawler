# -*-coding:utf-8-*-
import pytz
import redis
import scrapy
from scrapy.spiders import Spider
import pyreBloom
from base.configs.settings import REDIS_HOST, REDIS_PORT
from base.items.baidusousuo.items import ScrapyBaiduItem
from base.configs.baidusousuo.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_TABLE, MYSQL_USER, MYSQL_PASSWORD, KEYWORD_INDEX, SPIDER_COUNTS
import time
import datetime
import MySQLdb
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

class BaiduSpider(Spider):
    name = 'spider'
    def __init__(self):
        # self.bf = BloomFilter(0.0001, 100000)
        self.tz = pytz.timezone( 'Asia/Shanghai' )
        #r = redis.Redis( host=REDIS_HOST, port=REDIS_PORT)#, db = 0)
        self.r = redis.StrictRedis( host=REDIS_HOST, port=REDIS_PORT)
        # self.bf = pyreBloom.pyreBloom( 'baidusousuo', 100000, 0.0001, host=REDIS_HOST, port=REDIS_PORT )
        # print r.exists( "baidusousuo.0" )
        # print r.keys()
        if self.r.exists("baidusousuo.0"):
            print "baidusousuo.0 exist"
            self.bf = pyreBloom.pyreBloom( 'baidusousuo', 100000, 0.001, host=REDIS_HOST, port=REDIS_PORT )
            print self.r.ttl( 'baidusousuo.0' )
        else:
            print "creat baidusousuo.0"
            # r.set('baidusousuo.0','')
            self.bf = pyreBloom.pyreBloom( "baidusousuo", 100000, 0.001, host=REDIS_HOST, port=REDIS_PORT )
            tests = "Hello baidu!"
            self.bf.extend( tests )
            print self.r.expire( 'baidusousuo.0', 60*60*24*3 )
            time.sleep(3)

            # print self.bf.contains( 'hello' )
            # # True
            # print self.bf.contains( ['hello', 'whats', 'new', 'with', 'you'] )
            # # ['hello', 'you']
            # print 'hello' in self.bf
            # print self.r.get('baidusousuo')
            print self.r.ttl( 'baidusousuo.0' )

    def start_requests(self):
        # os.environ["all_proxy"] = "http://dailaoshi:D9xvyfrgPwqBx39u@bh21.84684.net:21026"
        headers = {
            'Host': 'www.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            #'Cookie': 'BDUSS=mU5b0JMcDRsTG90WWpTaU1aS2Iyd2N4QjhDNDlDSXNGVHpqQ3I5RUcwMEZUTDFaTVFBQUFBJCQAAAAAAAAAAAEAAADIYkwTendt1cUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAW~lVkFv5VZa; BAIDUID=9E7D54EE7C5D10298D4BA6C6272F4311:FG=1; BIDUPSID=6A549A7B4CFCB978124826509C41AD0C; PSTM=1509457426; MCITY=-233%3A; ispeed_lsm=1; BD_UPN=1352; ispeed=1; H_PS_PSSID=1435_21090_17001_20927; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; sugstore=1; BD_CK_SAM=1; PSINO=1; BDSVRTM=0',
            #'Connection': 'keep-alive',
            #'Upgrade-Insecure-Requests': '1'
        }
        # keywords = ['提供', '发现',  '研考', '硕士考试', '硕士生考试', '成考', '成人高考', '自考', '自学考试']
        while 1:
            db = MySQLdb.connect( host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                                  db=MYSQL_DATABASE, charset='utf8' )
            cursor = db.cursor()
            sql = "SELECT DISTINCT name FROM keyword_t"
            cursor.execute( sql )
            keywords = cursor.fetchall()
            d = datetime.datetime.now(self.tz)
            d1 = d.replace( hour=0, minute=0, second=0, microsecond=0 )
            d2 = d1 - datetime.timedelta( days=3 )
            t1 = int( time.mktime( d1.timetuple() ) )
            t2 = int( time.mktime( d2.timetuple() ) )
            url_p1 = 'https://www.baidu.com/s?wd='
            url_p2 = '&pn='
            url_p3 = '&gpc=stf%3D' + str( t2 ) + '%2C' + str( t1 ) + '|stftype%3D2'
            # for i, keyword in enumerate(keywords[::-1]):
            #     print keyword
            #     if i%10==KEYWORD_INDEX:
            #         print i, keyword
            for i in range( 20, 0, -1 ):
                # print i
                index = 0
                for keyword in keywords[::-1]:
                    # print keyword[0]
                    if index % SPIDER_COUNTS == KEYWORD_INDEX:
                        url = url_p1 + keyword[0] + url_p2 + str( i*10 ) +url_p3
                        time.sleep( 1 )
                        print index, keyword[0], url
                        yield scrapy.Request( url=url, headers=headers, dont_filter=True, callback=self.parse,
                                              meta={'keyword': keyword[0]} )
                    index += 1

    def parse(self, response):
        # print response.text
        keyword = response.meta['keyword']
        results = response.xpath('//div[@class="result c-container "]')
        #print results
        time = datetime.datetime.now(self.tz)
        for res in results:
            #print res.extract()
            url = res.xpath('.//h3[contains(@class,"t")]/a/@href').extract_first()
            # print keyword,url
            bfdata = str(keyword) + str(url)
            print self.r.ttl( 'baidusousuo.0' ),
            if self.r.ttl('baidusousuo.0') < 0:
                print self.r.exists('baidusousuo.0'),
                self.bf = pyreBloom.pyreBloom( "baidusousuo", 100000, 0.0001, host=REDIS_HOST, port=REDIS_PORT )
                # tests = "Hello baidu!"
                # self.bf.extend( tests )
                print self.r.expire( 'baidusousuo.0', 60*60*24*3 )
            if (self.bf.contains(str(bfdata)) == False):
                self.bf.extend(str(bfdata))
                item = ScrapyBaiduItem()
                item['url'] = url
                print url
                item['title'] = res.xpath('.//h3[contains(@class,"t")]/a').xpath('string(.)').extract_first()
                timestr = res.xpath( './/span[contains(@class," newTimeFactor_before_abs m")]' ).xpath(
                    'string(.)' ).extract_first()
                # print timestr
                if timestr == None:
                    item['time'] = time.strftime( '%Y_%m_%d_%H_%M_%S' )
                else:
                    if str( timestr ).find( '天前' ) != -1:
                        time_num = int( timestr[:str( timestr ).find( '天前' )] )
                        delta = datetime.timedelta( days=time_num )
                        new_time = time - delta
                        item['time'] = new_time.strftime( '%Y_%m_%d_%H_%M_%S' )
                    elif str( timestr ).find( '小时前' ) != -1:
                        time_num = int( timestr[:str( timestr ).find( '小时前' )] )
                        delta = datetime.timedelta( hours=time_num )
                        new_time = time - delta
                        item['time'] = new_time.strftime( '%Y_%m_%d_%H_%M_%S' )
                    elif str( timestr ).find( '分钟前' ) != -1:
                        time_num = int( timestr[:str( timestr ).find( '分钟前' )] )
                        delta = datetime.timedelta( minutes=time_num )
                        new_time = time - delta
                        item['time'] = new_time.strftime( '%Y_%m_%d_%H_%M_%S' )
                    elif str( timestr ).find( '秒钟前' ) != -1:
                        time_num = int( timestr[:str( timestr ).find( '秒钟前' )] )
                        delta = datetime.timedelta( seconds=time_num )
                        new_time = time - delta
                        item['time'] = new_time.strftime( '%Y_%m_%d_%H_%M_%S' )
                #print title
                abstract = res.xpath('.//div[contains(@class,"c-abstract")]').xpath('string(.)').extract_first()
                if abstract == None:
                    #print res.extract()
                    abstract = res.xpath('.//div[@class="c-span18 c-span-last"]/font/p').xpath('string(.)').extract()
                    abstract = ' '.join(abstract)
                    #print abstract
                #print abstract
                s = abstract.find( '-' )
                if s > 0:
                    abstract = abstract[s + 2:]
                item['abstract'] = abstract
                item['keyword'] = unicode(keyword)
                item['create_time'] = time.strftime('%Y_%m_%d_%H_%M_%S')
                yield item
