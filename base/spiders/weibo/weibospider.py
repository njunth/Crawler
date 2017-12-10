#!/usr/bin/python
# -*-coding:utf-8-*-
from scrapy.spiders import Spider
import urllib
import scrapy
import json
import re
import time
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
        keywords = ['出售', '提供', '发现', '高考', '考研', '研考', '硕士考试', '硕士生考试', '成考', '成人高考', '自考', '自学考试']
        url_p1 = 'https://m.weibo.cn/api/container/getIndex?type=wb&queryVal='
        url_p2 = '&featurecode=20000320&luicode=10000011&lfid=106003type%3D1&title='
        url_p3 = '&containerid=100103type%3D2%26q%3D'
        url_p4 = '&page='
        urls = []
        while 1:
            for keyword in keywords:
                print keyword
                key = urllib.quote(keyword)
                for i in range(1, 200):
                    url = url_p1 + key + url_p2 + key + url_p3 + key + url_p4 + str(i)
                    # print key
                    time.sleep(0.1)
                    yield scrapy.Request(url=url, callback=self.parse_search, headers=headers)

    def parse_search(self, response):
        #print response.status
        #print str(response.text)
        keyword = str(response.url)
        pos = keyword.index("&featurecode")
        keyword = urllib.unquote(keyword[59:pos])
        #print keyword
        #print 'unicode',isinstance(response.body,unicode)
        res = json.loads(response.text)
        if (str(res['ok']) == '1'):
            # print res
            # print res['data']['cards']
            for key in res['data']['cards'][0]['card_group']:
                ''''''
                print 111
                time.sleep(0.1)
                #yield item
                yield scrapy.Request(url=key['scheme'],callback=self.parse)
        else:
            # i=i-1
            if ('msg' in res.keys()):
                print res['msg']

    def parse(self, response):
        keyword = urllib.unquote(response.url)
        spos = keyword.find('&q=')
        epos = keyword.find('&featurecode')
        keyword = keyword[spos+3:epos]
        print 'successfully crawl'
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
        #item['url'] = key['status']['scheme']
        item['url'] = response.url
        item['authid'] = key['status']['user']['screen_name']
        yield item

