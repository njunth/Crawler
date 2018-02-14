# -*- coding: utf-8 -*-
import scrapy
import re
import sys
from base.items.xinhua_menhu.items import XinhuaScrapyItem
from base.items.xinhua_menhu.bloomfilter import BloomFilter
import datetime, random, time
class DmozSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["xinhuanet.com"]
    start_urls = [
        "http://www.xinhuanet.com"
        #"http://www.sd.xinhuanet.com"
    ]
    bf = BloomFilter(0.1, 10)
    #r1 = '^http://.*.cnr.*'
    #r2 = '^http://.*.cnr.*.shtml.*'
    #r3 = '^http://.*.cnr.*.html.*'
    #r4 = '^http://.*.cnr.*.htm.*'

    r1 = '^http://.*.xinhuanet.*'
    r2 = '^http://.*.xinhuanet.*.htm'
    r3 = '^http://.*.xinhuanet.*.index.htm'
    r4='^http://jp.xinhuanet.*'
    r5 = '^http://kr.xinhuanet.*'
    r6 = '^http://spanish.xinhuanet.*'
    r7 = '^http://french.xinhuanet.*'
    r8 = '^http://russian.xinhuanet.*'
    r9 = '^http://arabic.xinhuanet.*'
    r10 = '^http://german.xinhuanet.*'
    r11 = '^http://portuguese.xinhuanet.*'
    r12 = '^http://uyghur.xinhuanet.*'
    r13 = '^http://xizang.xinhuanet.*'
    r14 = '^http://mongolian.xinhuanet.*'
    r_language = r4+'|' + r5 + '|' + r6 + '|' + r7 + '|' + r8 + '|' + r9 + '|' + r10 + '|' + r11 + '|' + r12 + '|' + r13 + '|' + r14
    def start_requests(self):
        while 1:
            yield scrapy.Request("http://www.xinhuanet.com",callback=self.parse_mainpage)

    def parse_inpage(self, response):
        url = response.url
        #print url
        sleep_time = random.random()
        print sleep_time
        time.sleep( sleep_time )
        flag=0
        if re.match(self.r2, url):
            try:
                #print url
                self.bf.insert_element(url)
                #print "aaaaaaa!!!!!!!@*#()@_______"
                #for sel in response:
                item = XinhuaScrapyItem()
                # item['name'] = sel.xpath("h1[@class='main-title']/text()").extract()[0].encode('utf-8')
                # name= item['name']
                item['url'] = url

                item['title'] = response.xpath("//head/title/text()").extract_first()


                #print "qqqqqq"
                item['source'] = "新华网"
                item['source_url'] = "http://www.xinhuanet.com/"

                #try:
                item['html'] = ''
                contentlist = response.xpath('//html').extract()
                for con in contentlist:
                    utfcontent = con.encode('utf-8')
                    item['html'] += utfcontent
                #except:
                #item['html'] = response.body


                item['content'] = response.xpath("//div[@class='main']//p/text()").extract()
                if len(item['content'])==0:
                    item['content'] = response.xpath("//div[@class='article']//p/text()").extract()
                if len(item['content'])==0:
                    item['content'] = response.xpath("//div[@class='content']//p/text()").extract()
                if len(item['content']) == 0:
                    item['content'] = response.xpath("//div[@id='content']//p/text()").extract()
                if len(item['content']) == 0:
                    item['content'] = response.xpath("//div[@id='Content']//p/text()").extract()
                if len(item['content']) == 0:
                    item['content'] = response.xpath("//div[@class='zw_pic']//p/text()").extract()
                if len(item['content']) == 0:
                    item['content'] = response.xpath("//div[@class='main_content']//p/text()").extract()
                if len(item['content']) == 0:
                    item['content'] = response.xpath("//div[@class='zw']//p/text()").extract()

                item['content'] = ''.join(item['content'])


                time_item = []
                publish_time = response.xpath("normalize-space(//span[@class='h-time']/text())").extract()[0]
                if len(publish_time) == 0:
                    publish_time = response.xpath("normalize-space(//div[@class='head_detail']/text())").extract()[0]
                if len(publish_time) == 0:
                    publish_time = response.xpath("normalize-space(//div[@class='time']/text())").extract()[0]
                if len(publish_time) == 0:
                    publish_time = response.xpath("normalize-space(//div[@class='sj']/text())").extract()[0]
                if len(publish_time) == 0:
                    publish_time = response.xpath("normalize-space(//div[@class='source']/text())").extract()[0]
                if len(publish_time) == 0:
                    publish_time = response.xpath("normalize-space(//span[@class='time']/text())").extract()[0]
                if len(publish_time) == 0:
                    publish_time = response.xpath("normalize-space(//span[@id='pubtime']/text())").extract()[0]
                if len(publish_time) == 0:
                    publish_time = response.xpath("normalize-space(//div[@class='info']/text())").extract()[0]
                #time1 = response.xpath("//body//div[@class='source']/span").extract()
                # time1 = response.xpath("//head/meta[@property='article:published_time']//@content").extract()[1]
                if re.match(u'.*年.*',publish_time):
                    #print"aaafsssssssss"
                    flag=1
                # print time

                #print time1
                #print '/n'
                #print publish_time
                if flag==0:
                    time_item.append(publish_time[0:4])
                    time_item += '_'
                    time_item += publish_time[5:7]
                    time_item += '_'
                    time_item += publish_time[8:10]
                    time_item += '_'
                    time_item += publish_time[11:13]
                    time_item += '_'
                    time_item += publish_time[14:16]
                    time_item = ''.join(time_item)
                    item['time'] = time_item
                else:
                    time_item.append(publish_time[0:4])
                    time_item += '_'
                    time_item += publish_time[5:7]
                    time_item += '_'
                    time_item += publish_time[8:10]
                    time_item += '_'
                    time_item += publish_time[12:14]
                    time_item += '_'
                    time_item += publish_time[15:17]
                    time_item = ''.join(time_item)
                    item['time'] = time_item

                item['sentiment'] = 0
                item['attention'] = 0
                # print name
                #with open('aaa', 'ab') as f:
                    #f.write(response.url)
                    #f.write('\n')
                item['create_time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                if publish_time and item['content']:
                    #with open('aaa', 'ab') as f:
                        #f.write(response.url + '\n')
                        #f.write(item['time']+'\n')

                    yield item
                else:
                    #with open('aaa', 'ab') as f:
                        #f.write(response.url + '\n')
                    pass

            except:
                #with open('aaaa', 'ab') as f:
                    #f.write(response.url+'\n')
                #print(sys.exc_info())
                #with open('aa', 'ab') as f:
                    #f.write(response.url + '\n')
                pass

    def parse_mainpage(self, response):
                """
                with open('aaaa', 'ab') as f:
                    f.write(response.url)
                    f.write('\n')
"""
                for url in response.selector.xpath("//a/@href").re(self.r1):
                    if re.match(self.r4, url) is None and re.match(self.r5, url) is None and re.match(self.r_language, url) is None:
                        if re.match(self.r2, url) is None or re.match(self.r3,url):
                                yield scrapy.Request(url=url, callback=self.parse_mainpage,priority=0)
                        else:
                            if (self.bf.is_element_exist(url) == False):
                                yield scrapy.Request(url=url, callback=self.parse_inpage,priority=1)

