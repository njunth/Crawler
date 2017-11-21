#-*-coding:utf8-*-
import scrapy
from base.items.sina.items import SinaItem
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from base.items.sina.bloomfilter import BloomFilter

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

        item = SinaItem()

        if re.match('^http://club.[a-z.]*.sina.*.html', response.url):
            item['source'] = '新浪论坛'
            item['source_url'] = 'http://people.sina.com.cn/'
            try:
                item['html'] = response.body.decode('gbk')
            except:
                item['html'] = response.body
            item['url'] = response.url

            item['title'] = response.xpath("//head/title/text()").extract()[0].encode('utf-8')
            item['content'] = response.xpath("//div[@class='maincont']//p/text()").extract()

            # item['n_click'] = 0

            # n_click = 0
            # item['n_click'] = response.xpath("//div[@class='maincont']//tbody//span/font/text()").extract_first()
            n_click = response.xpath("//div[@class='maincont']//tbody//span/font/text()").extract_first()
            # if(n_click== 'none'):
            #   n_click = '0'

            nclick = ''.join(n_click)
            item['n_click'] = int(nclick)

            n_reply = response.xpath("//div[@class='maincont']//tbody//span/font/text()").extract()[1]
            # item['n_reply'] = response.xpath("//div[@class='maincont']//tbody//span/font/text()").extract()[1]
            # if (n_reply == 'none'):
            #   n_reply = '0'
            nreply = ''.join(n_reply)
            item['n_reply'] = int(nreply)

            time_item = []
            # item['time'] = response.xpath("//div[@class='maincont']//tbody//font/text()").extract()
            time = response.xpath("//div[@class='maincont']//tbody//font/text()").extract_first()
            time_item.append(time[4:8])
            time_item.append('_')
            time_item.append(time[9:11])
            time_item.append('_')
            time_item.append(time[12:14])
            time_item.append('_')
            time_item.append(time[15:17])
            time_item.append('_')
            time_item.append(time[18:20])
            # time_item.append('_')


            timeitem = ''.join(time_item)
            item['time'] = timeitem

            item['sentiment'] = 0
            item['attention'] = 0

            yield item
            self.bf.insert_element(response.url)

        for url1 in response.selector.xpath("//a/@href").re(r'^http://club.[a-z.]*.sina.*'):
            if (self.bf.is_element_exist(url1) == False):  # reduce a /
                yield scrapy.Request(url=url1, callback=self.parse)
            else:
                continue