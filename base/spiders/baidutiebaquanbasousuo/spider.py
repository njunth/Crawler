#encoding=utf-8
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from base.items.baidutiebaquanbasousuo.items import BaidutiebaquanbasousuoItem
# from base.items.baidutiebaquanbasousuo.bloomfliter import BloomFilter
from base.configs.baidutiebaquanbasousuo.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_TABLE, MYSQL_USER, MYSQL_PASSWORD, SPIDER_COUNTS, KEYWORD_INDEX

from datetime import datetime
import os, random, time
import urllib, MySQLdb
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class BaidutiebaquanbasousuoSpider(Spider):
    name = 'spider'
    allowed_domains=["tieba.baidu.com"]


    def __init__(self, name=None, **kwargs):

        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []
        self.mainpage="http://www.csbiji.com/forum.php"
        os.environ["all_proxy"]="http://dailaoshi:D9xvyfrgPwqBx39u@bh21.84684.net:21026"


    def start_requests(self):

        # keywords = ['出售', '提供', '发现', '高考', '考研', '研考', '硕士考试', '硕士生考试', '成考', '成人高考', '自考', '自学考试']
        url_p1 = 'http://tieba.baidu.com/f/search/res?isnew=1&kw=&qw='
        url_p2 = '&rn=10&un=&only_thread=0&sm=1&sd=&ed=&pn='
        while 1:
            # print MYSQL_HOST
            db = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DATABASE, charset='utf8')
            cursor = db.cursor()
            sql = "SELECT DISTINCT * FROM keyword_t"
            cursor.execute( sql )
            keywords = cursor.fetchall()

            for i in range(20, 0, -1):
                # print keyword[1].decode('utf-8')
                # key = urllib.quote(keyword)
                index = 0
                for keyword in keywords[::-1]:
                    key = keyword[1]
                    # print keyword[1].decode( 'utf-8' )
                    if index % SPIDER_COUNTS == KEYWORD_INDEX:
                        print index, keyword[1]
                        url = url_p1 + key + url_p2 + str(i)
                        yield Request(url=url, callback=self.parse_inPage, dont_filter=True)
                        sleep_time = random.random()
                        print 5 * sleep_time
                        time.sleep( 5 * sleep_time )
                    index += 1
            db.close()
            print "sleep 10s"
            time.sleep(10)

    def parse_inPage(self,response):
        url = response.url
        # sleep_time = random.random()
        # print 5*sleep_time
        # time.sleep( 5*sleep_time )
        print url
        item =BaidutiebaquanbasousuoItem()
        content_div1 = response.selector.xpath('//div[@class="p_content"]')
        content1 = content_div1.xpath('string(.)').extract()
        try:
            if (len(content1)>0):
                source_str=response.selector.xpath('//font[@class="p_violet"]')
                source_str1 = source_str.xpath('string(.)').extract()
                source_list=list()
                authid_list=list()
                i=0
                for t in source_str1:
                    if(i%2==0):
                        source_list.append(t)
                    else:
                        authid_list.append(t)
                    i=i+1
                #print len(source_list)
                #print len(authid_list)
                #os.system("pause")
                item['source']="百度贴吧".decode('utf-8')
                item['authid']=authid_list
                #print item['source']
                #print item['authid']
                item['url']=response.selector.xpath("//a[@data-tid and @data-fid]/@href").extract()
                #print item['source_url']
                #os.system("pause")
                item['source_url']="https://tieba.baidu.com/index.html"
                # item['html']=response.body.decode("unicode_escape")
                item['html'] = ''
                item['n_click']=0
                item['n_reply']=0
                item['content'] = content1
                title_div1 = response.selector.xpath('//a[@data-tid and @data-fid]')
                title1=title_div1.xpath('string(.)').extract()
                item['title'] =title1
                item['attention'] = 0
                time_str=response.selector.xpath("//font[@class='p_green p_date']/text()").extract()
                item['time']=time_str
                item['sentiment']=0
                item['create_time']=str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
                yield item
        except:
            print('error')
