# coding=utf-8
import scrapy
from base.items.qiangguo.items import QiangguoItem
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from base.items.qiangguo.bloomfilter import BloomFilter
import datetime, random, time
import string


class Tianyaspider(scrapy.Spider):
    name = "spider"

    allowed_domins = ["people.com.cn"]

    start_urls = {
        "http://bbs1.people.com.cn/"
    }
    bf = BloomFilter(0.0001, 100000)

    def parse(self, response):

        while 1:
            for url1 in response.selector.xpath("//a/@href").re(r'^http://bbs1.people.com.cn.*.html'):
            #if (self.bf.is_element_exist(url1) == False):
                yield scrapy.Request(url=url1, callback=self.parse_inpage)
            #else:
             #   continue

    def parse_inpage(self, response):
        sleep_time = random.random()
        print sleep_time
        time.sleep( sleep_time )
        item = QiangguoItem()
        #item['content'] = response.xpath("//p//text()").extract()
        content = response.selector.xpath("//div//p")
        con_div = content.xpath('string(.)').extract()
        print response.url


        if re.match('^http://bbs1.people.com.cn.*.html', response.url) and len(con_div) > 0:
            item['source'] = "强国论坛"
            item['source_url'] = 'http://bbs1.people.com.cn/'

            item['html'] = ''
            contentlist = response.xpath('//html').extract()
            for con in contentlist:
                utfcontent = con.encode('utf-8')
                item['html'] += utfcontent

            item['url'] = response.url
            item['create_time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            item['sentiment'] = 0
            item['attention'] = 0
            #item['n_click'] = response.xpath("//span[@class='readNum']//text()").extract()
            n_click = response.xpath("//span[@class='readNum']//text()").extract()
            #item['n_reply'] = response.xpath("//span[@class='replayNum']//text()").extract()
            n_reply = response.xpath("//span[@class='replayNum']//text()").extract()
            item['authid'] = response.xpath("//a[@class='userNick']//text()").extract()
            item['replies'] = response.xpath("//a[@class='treeReply']//text()").extract()
            item['title'] = response.xpath("//h2//text()").extract_first()

            #item['content'] = response.xpath("//p/text()").extract()
            item['content'] = con_div

            #item['content'] = response.selector.xpath("//p//font//text()").extract()
            #item['content'] = response.xpath("//*[@id='post_content_165530055']/p[3]/font").extract()

            #item['time'] = response.xpath("//p[@class='replayInfo']//text()").extract()
            item['time'] = response.xpath("//p//span//text()").extract()
            #item['time'] = response.xpath("//span[@class='float_l mT10']//text()").extract()[4]

            if n_click is None:
                item['n_click'] = 0
            else:
                nclick = ''.join(n_click)
                nc = nclick
                for c in string.punctuation:
                    nc = nc.replace(c, '')

                if nc is None or nc is '':
                    item['n_click'] = 0
                else:
                    item['n_click'] = int(nc)

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

            yield item
            #self.bf.insert_element(response.url)
