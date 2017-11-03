#-*-coding:utf8-*-
import scrapy
from base.items.sina.items import SinaItem
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

class Sinaspider(scrapy.Spider):
    name =  "spider"

    allowed_domins = ["sina.com.cn"]

    start_urls = {
        "http://people.sina.com.cn/"
    }


    def parse(self,response):

        item = SinaItem()
        #try:

        if re.match('^http://[a-z.]*.sina.*.html', response.url):
            item['source'] = '新浪论坛'
            item['mainpage'] = 'http://people.sina.com.cn/'
            item['content'] = response.body
            item['link'] = response.url

            yield item

            #link = response.xpath("//a/@href").extract()
        #link= response.body



        for url1 in response.selector.xpath("//a/@href").re(r'^http://[a-z.]*.sina.*'):
            yield scrapy.Request(url=url1, callback=self.parse)


        #links = LinkExtractor(allow=()).extract_links(response)
        #for link in links:
         #   if "//.html" in link.url:  # 如果是包含“//ent.sina.com.cn”的url，那么对其继续连接爬取分析
          #      yield scrapy.Request(url=link.url, callback=self.parse_page)

                #except:
         #   print("error")
