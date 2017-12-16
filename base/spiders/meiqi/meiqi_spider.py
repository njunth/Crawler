# -*-coding:utf8-*-
import scrapy
from base.items.meiqi.items import MeiqiItem
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from base.items.meiqi.BloomFilter import BloomFilter
import string
import datetime, random, time


class Meiqispider(scrapy.Spider):
    name = "spider"

    allowed_domins = ["biketo.com"]

    start_urls = {
        "http://bbs.biketo.com/index.html"
        # "http://bbs.biketo.com/index.html"
    }
    #bf = BloomFilter(0.0001, 1000000)

    def parse(self, response):

        while 1:
            # url = response.xpath("//a/@href").extract()
            for url1 in response.selector.xpath("//a/@href").re(r'^http://bbs.biketo.com.*.html'):
                # for url1 in url:
                #if (self.bf.is_element_exist(url1) == False):  # reduce a /
                sleep_time = random.random()
                print sleep_time
                time.sleep( sleep_time )
                yield scrapy.Request(url=url1, callback=self.parse_inpage)
                #else:
                    #continue
                 #   yield scrapy.Request(url=url1, callback=self.parse)

            #for url in response.selector.xpath("//a/@href").re(r'^http://bbs.biketo.com.*.html'):
             #   if re.match('^http://bbs.biketo.com.*.html', url) is None:
              #      yield scrapy.Request(url=url, callback=self.parse)

    def parse_inpage(self, response):
        item = MeiqiItem()
        content = response.selector.xpath("//div[@class='t_fsz']//td[@class='t_f']")#/text()").extract()
        con_div = content.xpath('string(.)').extract()

        if re.match('^http://bbs.biketo.com.*.html', response.url) and len(con_div)>0:
            item['source'] = "美骑社区"
            item['source_url'] = 'http://bbs.biketo.com/index.html'

            item['html'] = ''
            contentlist = response.xpath('//html').extract()
            for con in contentlist:
                utfcontent = con.encode('utf-8')
                item['html'] += utfcontent

            item['url'] = response.url

            t = response.xpath(
                "//div[@id='postlist']//span[@id='thread_subject']/text()").extract()  # [0].encode('utf-8')
            title = ''.join(t)
            title1 = title.encode('utf-8')
            item['title'] = title1

            #content = response.xpath("//div[@class='t_fsz']//td[@class='t_f']/text()").extract()
            #content1 = ''.join(content)
            #item['content'] = content1  # response.xpath("//div[@class='t_fsz']//td[@class='t_f']/text()").extract()
            item['content'] = con_div
            item['mainauth'] = response.xpath("//a[@target='_blank'][@class='xw1']/text()").extract_first()
            item['authid'] = response.xpath("//a[@target='_blank'][@class='xg1']/text()").extract()
            item['testtime'] = response.xpath("//em[@class='date']/text()").extract()




            time_item = []
            time = response.xpath("//div[@class='pti']//em/text()").extract_first()
            # item['time'] = time
            if (time == None):
                item['time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            else:
                time_item.append(time[0:4])
                time_item.append('_')
                if (time[6] == '-'):
                    time_item.append('0')
                    time_item.append(time[5])
                else:
                    time_item.append(time[5:7])

                # 2016-(5)4-(7)7   8
                # 2016-(56)12-(8)7  not 8
                # 2016-(5)4-(78)17  not 8
                # 2016-(56)12-(89)17

                time_item.append('_')
                if (time[7] == '-'):
                    if (time[9] == ' '):
                        time_item.append('0')
                        time_item.append(time[8])
                    else:
                        time_item.append(time[8:10])
                else:
                    if (time[8] == ' '):
                        time_item.append('0')
                        time_item.append(time[7])
                    else:
                        time_item.append(time[7:9])

                time_item.append('_')
                time_item.append(time[len(time) - 5])
                time_item.append(time[len(time) - 4])
                time_item.append('_')
                time_item.append(time[len(time) - 2])
                time_item.append(time[len(time) - 1])

                timeitem = ''.join(time_item)

                item['time'] = timeitem

            n_click = response.xpath("//div[@class='pti']//em[@class='views']/text()").extract_first()
            if (n_click != None):
                nclick = ''.join(n_click)
            else:
                nclick = None

            if (nclick == None):
                item['n_click'] = 0
            else:
                item['n_click'] = int(nclick)

            n_reply = response.xpath("//div[@class='pti']//em[@class='replies']/text()").extract_first()
            if (n_reply != None):
                nreply = ''.join(n_reply)
            else:
                nreply = None

            if (nreply == None):
                item['n_reply'] = 0
            else:
                item['n_reply'] = int(nreply)

            item['sentiment'] = 0
            item['attention'] = 0

            # if(response.url != 'http://bbs.biketo.com/index.html'):
            #self.bf.insert_element(response.url)
            yield item









