#-*-coding:utf8-*-
import scrapy
from base.items.yanjiao.items import YanjiaoItem
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from base.items.sina.bloomfilter import BloomFilter
import string
import datetime, random, time

class yanjiaoSpider(scrapy.Spider):
    name = "spider"

    allowed_domins = ["yanjiao.com"]

    start_urls = {
        "http://www.yanjiao.com/portal.php"
        #"http://people.sina.com.cn/"
        # "http://club.eladies.sina.com.cn/thread-6490945-1-1.html"
        # "http://club.eladies.sina.com.cn/thread-6596256-1-1.html"
    }

    bf = BloomFilter(0.0001,1000000)

    #def start_requests(self):
     #   while 1:
      #      yield scrapy.Request("http://www.yanjiao.com/portal.php", callback=self.parse_mainPage)
    r1 = '^www.yanjiao.com/forum.php?mod=viewthread&tid=[0-9]+.*'
    #r1 = '.*.tid*.*'
    r2 = '^http://www.yanjiao.com.thread.*.[0-9]+'

    def parse(self, response):

        #while 1:
        #item = SinaItem()
        r3='.*.thread.*'
        r4='^http://www.yanjiao.com.*'
        r5= r3+'|'+r4
        while 1:
            for url1 in response.selector.xpath("//a/@href").re(r5):
                sleep_time = random.random()
                #print sleep_time
                time.sleep(sleep_time)

                if not url1.startswith('http'):
                    url1 = "http://www.yanjiao.com" + url1


                if re.match(self.r1, url1) or re.match(self.r2, url1):  # reduce a /
                    yield scrapy.Request(url=url1, callback=self.parse_inpage,priority=1)
                else:
                    yield scrapy.Request(url=url1, callback=self.parse,priority=0)
                #else:
                    #continue
                #yield scrapy.Request(url=url1, callback=self.parse)

            #for url1 in response.selector.xpath("//a/@href").re(r'^http://club.[a-z.]*.sina.*'):
             #   yield scrapy.Request(url=url1, callback=self.parse)


    def parse_inpage(self,response):

        item = YanjiaoItem()
        #reply = response.selector.xpath("//div[@class='cont f14']")#//text()")  # .extract()
        #reply1 = reply.xpath('string(.)').extract()
        content = response.xpath("//td[@class='t_f']//font")
        con_div = content.xpath('string(.)').extract()

        reply = response.xpath("//div[@class='t_fsz']//td[@class='t_f']")#.extract()
        reply_div = reply.xpath('string(.)').extract()


        r1 = '^www.yanjiao.com/forum.php?mod=viewthread&tid=[0-9]+'
        #r1 = '.*.tid*.*'
        r2 = '^http://www.yanjiao.com.thread.*.[0-9]+.*'

        if re.match(r1, response.url) or re.match(r2,response.url) and len(reply_div)>0:
            item['source'] = '燕郊网城'
            item['source_url'] = 'http://www.yanjiao.com/portal.php'

            item['html'] = ''
            contentlist = response.xpath('//html').extract()
            for con in contentlist:
                utfcontent = con.encode('utf-8')
                item['html'] += utfcontent


            item['url'] = response.url

            t = response.xpath("//span[@id='thread_subject']/text()").extract()#[0].encode('utf-8')
            title = ''.join(t)
            title1 = title.encode('utf-8')
            item['title'] = title1

            #try:
                #item['content']  = response.xpath("//div[@class='maincont']//p//text()").extract()
            item['content'] = response.xpath("//td[@class='t_f']//font//text()").extract()
            item['content'] = con_div
            #except:
                #item['content'] = response.xpath("//div[@class='postmessage defaultpost']//text()").extract()

            #item['replies'] =
            #reply = response.selector.xpath("//div[@class='cont f14']//text()")#.extract()
            #item['replies'] = response.xpath("//div[@class='cont f14']//text()").extract()
            #item['replies'] = reply.xpath('string(.)').extract()#response.xpath("//div[@class='cont f14']//text()").extract()#reply.xpath('string(.)').extract()
            #item['replies'] = reply1


            #item['replies'] = response.xpath("//div[@class='t_fsz']//td[@class='t_f']//text()").extract()
            item['replies'] = reply_div
            #item['replies'] = ''.join(item['replies'])
            #item['content'] = response.xpath("//tbody//p//font/text()").extract()

            #item['content'] = response.xpath("//div[@class='mybbs_cont']/text()").extract()
            #try:
             #   item['content'] = response.xpath("//div[@class='mainbox']//p//text()").extract()
            #except:
             #   item['content'] = response.xpath("//td[@class='postcontent']//text()").extract()


            #item['content'] = ''.join(item['content'])
            #try:
            item['authid'] = response.xpath("//div[@class='authi']//a[@class='xw1']//text()").extract()#不要first获得全部
            #except:
             #   item['authid'] = response.xpath("//td[@class='postauthor']/text()").extract()

            #item['authid'] = author1#''.join(item['authid'])


            #try:
            item['testtime'] = response.xpath("//div[@class='authi']//em/text()").extract()
            #except:
             #   item['testtime'] = response.xpath("//td[@class='postauthor']/text()").extract()
                #item['testtime'] = item['testtime'][3]

            #item['n_click'] = response.xpath("//span[@class='xi1']//text()").extract_first()
            #item['n_reply'] = response.xpath("//span[@class='xi1']//text()").extract()[1]


            n_click = response.xpath("//span[@class='xi1']//text()").extract_first()
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
            n_reply = response.xpath("//span[@class='xi1']//text()").extract()[1]

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



            """time_item = []
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
                item['time'] = timeitem"""

            item['sentiment'] = 0
            item['attention'] = 0

            yield item
            self.bf.insert_element(response.url)

        #res = response.xpath("//a/@href")
        #for url2 in res: #ponse.selector.xpath("//a/@href").re(r'^http://www.yanjiao.com.*'):
            #if re.match(r'^http://www.yanjiao.com.*', url2):
         #   yield scrapy.Request(url=url2, callback=self.parse_inpage)

