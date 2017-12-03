#-*-coding:utf8-*-
import scrapy
from base.items.sina.items import SinaItem
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from base.items.sina.bloomfilter import BloomFilter
import string
import datetime

class Sinaspider(scrapy.Spider):
    name = "spider"

    allowed_domins = ["sina.com.cn"]

    start_urls = {
        "http://people.sina.com.cn/"
        # "http://club.eladies.sina.com.cn/thread-6490945-1-1.html"
        # "http://club.eladies.sina.com.cn/thread-6596256-1-1.html"
    }
    bf = BloomFilter(0.1, 10)

    def parse(self, response):

        #while 1:
        #item = SinaItem()


        while 1:

            for url1 in response.selector.xpath("//a/@href").re(r'^http://club.[a-z.]*.sina.*'):
                if (self.bf.is_element_exist(url1) == False):  # reduce a /
                    yield scrapy.Request(url=url1, callback=self.parse_inpage)
                else:
                    #continue
                    yield scrapy.Request(url=url1, callback=self.parse)

            #for url1 in response.selector.xpath("//a/@href").re(r'^http://club.[a-z.]*.sina.*'):
             #   yield scrapy.Request(url=url1, callback=self.parse)


    def parse_inpage(self,response):
        item = SinaItem()
        if re.match('^http://club.[a-z.]*.sina.*.html', response.url):
            item['source'] = '新浪论坛'
            item['source_url'] = 'http://people.sina.com.cn/'

            item['html'] = ''
            contentlist = response.xpath('//html').extract()
            for con in contentlist:
                utfcontent = con.encode('utf-8')
                item['html'] += utfcontent
            titlelist = response.xpath('//title/text()').extract()

            """try:
                item['html'] = response.body.decode('gbk')
            except:
                item['html'] = response.body"""
            item['url'] = response.url

            #item['title'] = response.xpath("//head/title/text()").extract()[0].encode('utf-8')
            t = response.xpath("//head/title/text()").extract()#[0].encode('utf-8')
            title = ''.join(t)
            title1 = title.encode('utf-8')
            item['title'] = title1

            #item['content']  = response.xpath("//div[@class='maincont']//p/text()").extract()
            item['content'] = response.xpath("//tbody//p//font/text()").extract()

            item['content'] = ''.join(item['content'])

            n_click = response.xpath("//div[@class='maincont']//tbody//span/font/text()").extract_first()
            #item['n_click'] = n_click
            if n_click is None:
                item['n_click'] = 0
            else:
                nclick = ''.join(n_click)
                nc = nclick
                for c in string.punctuation:
                    nc = nc.replace(c, '')

                if nc is None:
                    item['n_click'] = 0
                else:
                    item['n_click'] = int(nc)


            #n_reply = response.xpath("//div[@class='maincont']//tbody//span/font/text()").extract()[1]
            n_reply = response.xpath("//div[@class='maincont']//span/font[2]/text()").extract()

            if n_reply is None:
                item['n_reply'] = 0
            else:
                nreply = ''.join(n_reply)
                nr = nreply
                for c in string.punctuation:
                    nr = nr.replace(c, '')

                if nr is None:
                    item['n_reply'] = 0
                else:
                    if nr is '':
                        item['n_reply'] = 0
                    else:
                        item['n_reply'] = int(nr)



            time_item = []
            time = response.xpath("//div[@class='maincont']//tbody//font/text()").extract_first()
            if time is None:
                item['time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            else:
                time_item.append(time[4:8])
                time_item.append('_')
                time_item.append(time[9:11])
                time_item.append('_')
                time_item.append(time[12:14])
                time_item.append('_')
                time_item.append(time[15:17])
                time_item.append('_')
                time_item.append(time[18:20])

                timeitem = ''.join(time_item)
                item['time'] = timeitem

            item['sentiment'] = 0
            item['attention'] = 0

            yield item
            self.bf.insert_element(response.url)

