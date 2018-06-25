import scrapy

import pytz
from base.items.mofcom.items import MyspiderItem
#class MofcomSpider(scrapy.Spider):
#    name = "Mofcom"
#    allowed_domains = "mofcom.gov.cn"
#    start_urls = ["http://www.mofcom.gov.cn/article/ae/"]

#    def parse(self, response):
 #       url = response.url
        #print url

class DmozSpider(scrapy.Spider):
    name = "Mofcom"
    allowed_domains = ["mofcom.gov.cn"]
    start_urls = [
        "http://www.mofcom.gov.cn/article/ae/"
    ]

    def __init__(self):
        # self.bf = BloomFilter(0.0001, 100000)
        #self.tz = pytz.timezone( 'Asia/Shanghai' )
        pass

    def parse(self, response):
        #filename = response.url.split("/")[-2] + '.html'
        #with open(filename, 'wb') as f:
          #  f.write(response.body)
        #items = []
        #results = response.selector.xpath('//head/meta').extract()

        #for re in results:
         #   url = re.xpath('.//@href').extract_first()
        #item = MyspiderItem()
        #item['url'] = response.selector.xpath('//head/@href').extract()
        #item['name'] = response.selector.xpath('//head/meta[@name="SiteName"]/@content').extract_first()
        #yield item
        hrefs = response.selector.xpath('//p[@class="pMore"]/a/@href')
        for href in hrefs:
            #print href
            site = response.urljoin("/".join(href.extract().split('/')[3:]))
            if not site.startswith('http'):
                url = "http://www.mofcom.gov.cn/article/ae/" + site
            else:
                url = site
            #print url
            yield scrapy.Request(url, callback=self.parse_more)

    def parse_more(self, response):
        for sel in response.xpath('//li/a'):
            item = MyspiderItem()
            item['title'] = sel.xpath('./@title').extract()
            site = sel.xpath('./@href').extract()[0]
            if not site.startswith('http'):
                url = "http://www.mofcom.gov.cn/article/ae" + site
            else:
                url = site
            item['link'] = url
            yield scrapy.Request(item['link'],callback=self.parse_desc,meta={'item': item})
            #item['desc'] = sel.xpath('./text()').extract()
            #item['time'] = sel.xpath('//a/')
            #yield item

    def parse_desc(self,response):
        item = response.meta['item']
        # populate more `item` fields
        sel = response.xpath('//div[@id="zoom"]/p[@style="TEXT-INDENT: 2em"]/text()').extract()
        item['desc'] = sel
        yield item
