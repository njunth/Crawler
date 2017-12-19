# -*- coding: utf-8 -*-
import scrapy
import re
from base.items.sina_menhu.items import SinaScrapyItem
from base.items.sina_menhu.bloomfilter import BloomFilter
import sys
import datetime, random, time
class DmozSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["sina.com.cn"]
    start_urls = [
        "http://www.sina.com.cn/"
        #"http://edu.sina.com.cn/"
    ]
    r1 = '^http://.*.sina.*'
    r2 = '^http://.*.sina.*.shtml.*'
    r3 = '^http://.*video.sina.*'
    r4 = '^http://.*auto.sina.*'
    r5 = '^http://.*.sina.*.html.*'
    r6='^http://.*blog.sina.*'
    r7='^http://.*slide.*.sina.*'
    r8='^http://.*jiaju.*.sina.*'
    bf = BloomFilter(0.0001, 1000000)
    def parse_inpage(self, response):
        r_content1="//div[@id='artibody']//p/text()"
        url = response.url
        sleep_time = random.random()
        print sleep_time
        time.sleep( sleep_time )
        # print url
        publish_time=[]
        try:
            if re.match(self.r2, url) or re.match(self.r5, url):
                # print "crawl"
                self.bf.insert_element(url)
                item = SinaScrapyItem()
                item['title'] = response.xpath("//head/title/text()").extract_first().encode('utf-8')
                #item['title'] = response.xpath("//h1/text()").extract_first().encode('utf-8')
                item['content']=response.xpath(r_content1).extract()
                item['content'] = ''.join(item['content'])
                # name= item['name']
                item['url'] = url
                item['sentiment'] = 0
                item['attention'] = 0

                item['html'] = ''
                contentlist = response.xpath('//html').extract()
                for con in contentlist:
                    utfcontent = con.encode('utf-8')
                    item['html'] += utfcontent

                item['source'] = "新浪网"
                item['source_url'] = "http://www.sina.com.cn/"
                #item['time']
                time_item=[]
                try:
                    publish_time= response.xpath("//head/meta[@property='article:published_time']/@content").extract()[0]
                #time1 = response.xpath("//head/meta[@property='article:published_time']//@content").extract()[1]
                    #print time
                except:
                    #print len(time)
                    try:
                        publish_time = response.xpath("//span[@class='timer']/text()").extract()[0]
                    except:
                        publish_time = response.xpath("//p[@class='source-time']/span/text()").extract()[0]

                    #print time
                time_item.append(publish_time[0:4])
                time_item += '_'
                time_item += publish_time[5:7]
                time_item += '_'
                time_item +=publish_time[8:10]
                time_item += '_'
                time_item += publish_time[11:13]
                time_item += '_'
                time_item += publish_time[14:16]
                time_item = ''.join(time_item)
                item['time'] = time_item
                item['create_time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

                #with open('aaa', 'ab') as f:
                  #f.write(response.url)
                  #f.write('\n')
                yield item
        except:
            #print url
            #print time
            #print '\n'
            #print(sys.exc_info())
            pass

    def parse(self, response):
        """
        with open('aaaa', 'ab') as f:
            f.write(response.url)
            f.write('\n')
            """
        for url in response.selector.xpath("//a/@href").re(self.r1):
            if re.match(self.r2, url) is None and re.match(self.r3, url) is None and re.match(self.r4, url) is None \
                    and re.match(self.r4, url) is None and re.match(self.r5, url) is None and re.match(self.r6, url) is None\
                    and re.match(self.r7, url) is None and re.match(self.r8, url) is None:
                yield scrapy.Request(url=url, callback=self.parse, priority=0, dont_filter=True)

            else:
                if re.match(self.r3, url) == None and re.match(self.r4, url) == None and re.match(self.r6, url) is None\
                    and re.match(self.r7, url) is None and re.match(self.r8, url) is None:
                    if (self.bf.is_element_exist(url) == False):

                        yield scrapy.Request(url=url, callback=self.parse_inpage, priority=1, dont_filter=True)