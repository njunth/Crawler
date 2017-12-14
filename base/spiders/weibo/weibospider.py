#!/usr/bin/python
# -*-coding:utf-8-*-
from scrapy.spiders import Spider
import urllib
import scrapy
import json
import re, MySQLdb
import time, random
import datetime
from base.configs.weibo.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_TABLE, MYSQL_USER, MYSQL_PASSWORD
from base.items.weibo.items import WeiboItem

class WeiboSpider(Spider):
    name = "spider"
    def start_requests(self):
        headers = {
            #    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            #    'Accept-Encoding':'gzip, deflate, br',
            #    'Accept-Language':'zh-CN,zh;q=0.8',
            #    'Connection':'keep-alive',
            #    'Host':'m.weibo.cn',
            #    'Upgrade-Insecure-Requests':'1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
        # keywords = ['高考', '出售', '提供', '发现', '考研', '研考', '硕士考试', '硕士生考试', '成考', '成人高考', '自考', '自学考试']
        # keywords = ['高考', '出售', '提供']
        url_p1 = 'https://m.weibo.cn/api/container/getIndex?type=wb&queryVal='
        url_p2 = '&featurecode=20000320&luicode=10000011&lfid=106003type%3D1&title='
        url_p3 = '&containerid=100103type%3D2%26q%3D'
        url_p4 = '&page='
        urls = []
        while 1:
            db = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DATABASE, charset='utf8')
            cursor = db.cursor()
            sql = "SELECT * FROM keyword_t"
            cursor.execute( sql )
            keywords = cursor.fetchall()
            for keyword in keywords[::-1]:
                print keyword[1].decode('utf-8')
                # print keyword
                key = keyword[1]
                for i in range(1, 50):
                    # print i
                    url = url_p1 + key + url_p2 + key + url_p3 + key + url_p4 + str(i)
                    yield scrapy.Request(url=url, callback=self.parse_search, headers=headers, dont_filter=True)
                    # print url
            db.close()
            print "sleep 10s"
            time.sleep(10)

    def parse_search(self, response):
        sleep_time = random.random()
        print 5*sleep_time
        time.sleep( 5*sleep_time )
        #print response.status
        #print str(response.text)
        keyword = str(response.url)
        pos = keyword.index("&featurecode")
        keyword = urllib.unquote(keyword[59:pos])
        #print keyword
        #print 'unicode',isinstance(response.body,unicode)
        res = json.loads(response.text)
        if (str(res['ok']) == '1'):
            for key in res['data']['cards'][0]['card_group']:
                item = WeiboItem()
                item['_id'] = key['mblog']['id']
                item['content'] = key['mblog']['text']
                # item['source'] = 'sina_weibo'
                item['n_forward'] = key['mblog']['reposts_count']
                item['n_comment'] = key['mblog']['comments_count']
                item['n_like'] = key['mblog']['attitudes_count']
                # item['attention'] = '0'
                # item['sentiment'] = '0'
                item['keyword'] = unicode(keyword)
                timestr = str(key['mblog']['created_at'])
                # print timestr
                d = datetime.datetime.now()
                if '分钟' in timestr:
                    minute = int(timestr[0:timestr.index('分钟')])
                    delta = datetime.timedelta(minutes=minute)
                    d = d - delta
                elif '小时' in timestr:
                    hour = int(timestr[0:timestr.index('小时')])
                    delta = datetime.timedelta(hours=hour)
                    d = d - delta
                elif '昨天' in timestr:
                    pos = timestr.index(':')
                    hour = int(timestr[pos - 2:pos])
                    minute = int(timestr[pos + 1:pos + 3])
                    delta = datetime.timedelta(days=1, hours=d.hour - hour, minutes=d.minute - minute)
                    d = d - delta
                elif '-' in timestr:
                    month = int(timestr[0:2])
                    day = int(timestr[3:5])
                    d = d.replace(month=month, day=day)
                item['time'] = d.strftime('%Y_%m_%d_%H_%M_%S')
                url_pos = key['scheme'].index("?mblogid")
                item['url'] = key['scheme'][0:url_pos]
                item['publisher'] = key['mblog']['user']['screen_name']
                yield item
                #yield scrapy.Request(url=key['scheme'],callback=self.parse)
        else:
            # i=i-1
            if ('msg' in res.keys()):
                print res['msg']

    '''def parse(self, response):
        time.sleep(1)
        keyword = urllib.unquote(response.url)
        spos = keyword.find('&q=')
        epos = keyword.find('&featurecode')
        keyword = keyword[spos+3:epos]
        #print keyword
        s = str(response.text)
        (st,end) = re.search('render_data = .+status.+\\}\\]\\[0\\] \\|\\| \\{\\};',s,re.S).span()
        s = s[st+15:end-11]
        key = json.loads(s)
        timestrs = str(key['status']['created_at']).split(' ')
        timestr = timestrs[5] + ' ' + timestrs[1] + ' ' + timestrs[2] + ' ' + timestrs[3]
        timestr = time.strftime('%Y_%m_%d_%H_%M_%S',time.strptime(timestr,'%Y %b %d %X'))
        item = WeiboItem()
        item['_id'] = key['status']['id']
        item['content'] = key['status']['text']
        # item['source'] = 'sina_weibo'
        item['n_forword'] = key['status']['reposts_count']
        item['n_comment'] = key['status']['comments_count']
        item['n_like'] = key['status']['attitudes_count']
        # item['attention'] = '0'
        # item['sentiment'] = '0'
        item['keyword'] = unicode(keyword)
        item['time'] = timestr
        item['url'] = key['status']['scheme']
        item['publisher'] = key['status']['user']['screen_name']
        yield item'''
