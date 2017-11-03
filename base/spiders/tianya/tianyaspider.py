#-*-coding:utf8-*-
import scrapy
from base.items.tianya.items import Tianyav2Item
import re



class Tianyaspider(scrapy.Spider):
    name =  "spider"

    allowed_domins = ["tianya.cn"]

    start_urls = {
        "http://bbs.tianya.cn/"
        #"http://bbs.tianya.cn/post-travel-821028-1.shtml"
    }


    def parse(self,response):

        item = Tianyav2Item()
        #try:
        item['source'] = '天涯'
        item['mainpage'] = 'http://bbs.tianya.cn/'
        item['content'] = response.body
        item['link'] = response.url

        yield item

        for url1 in response.selector.xpath("//li/div[@class='title']/a/@href").re(r'^http://bbs.tianya.*'):
            yield scrapy.Request(url=url1, callback=self.parse)
        #except:
         #   print("error")
