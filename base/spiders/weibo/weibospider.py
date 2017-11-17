#!/usr/bin/python
# -*-coding:utf-8-*-
from scrapy.spiders import Spider
import urllib
import scrapy
import json
import datetime
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
                key = urllib.quote(keyword)
                for i in range(1, 200):
                    url = url_p1 + key + url_p2 + key + url_p3 + key + url_p4 + str(i)
                    yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        #print response.status
        #print str(response.text)
        keyword = str(response.url)
        pos = keyword.index("&featurecode")
        keyword = urllib.unquote(keyword[59:pos])
        #print keyword
        #print 'unicode',isinstance(response.body,unicode)
        res = json.loads(response.text)
        if (str(res['ok']) == '1'):
            for key in res['cards'][0]['card_group']:
                #print key['mblog']['id'], key['mblog']['text'], key['mblog']['reposts_count'], key['mblog'][
                    #'comments_count'], key['mblog']['attitudes_count']
                item = WeiboItem()
                item['_id'] = key['mblog']['id']
                item['content'] = key['mblog']['text']
                #item['source'] = 'sina_weibo'
                item['n_forword'] = key['mblog']['reposts_count']
                item['n_comment'] = key['mblog']['comments_count']
                item['n_like'] = key['mblog']['attitudes_count']
                #item['attention'] = '0'
                #item['sentiment'] = '0'
                item['keyword'] = unicode(keyword)
                item['time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '_' + key['mblog']['created_at']
                item['url'] = key['scheme']
                item['publisher'] = key['mblog']['user']['screen_name']
                yield item
        else:
            # i=i-1
            if ('msg' in res.keys()):
                print res['msg']

