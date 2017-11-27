import scrapy

from base.items.haitian.items import HaiItem
from scrapy.http import Request
import datetime
from base.items.haitian.BloomFilter import BloomFilter

class htkaoyan(scrapy.Spider):
	name="spider"
	allowed_domains=["www.htkaoyan.com"]

	start_urls=["http://www.htkaoyan.com"]

	def parse(self,response):
		self.bf=BloomFilter(0.0001,1000000)
		while 1:
			urls = response.xpath("//*/a[starts-with(@href,'http')]/@href").extract()
			for url in urls:
				if(self.bf.is_element_exist(url)==False):
					yield Request(url,callback=self.parse_inPage)
				else:
					continue

	def parse_inPage(self,response):

		item = HaiItem()
		item['title'] = ''
		item['source'] = "HaiTianKaoYan"
		item['source_url'] = "http://www.htkaoyan.com"
		item['url'] = response.url
		item['html'] = ''
		item['time'] = ''
		item['content'] = ''
		item['attention'] = 0
		item['sentiment'] = 0
		contentlist = response.xpath('//html').extract()

		for con in contentlist:
			utfcontent = con.encode('utf-8')
			item['html'] += utfcontent
		titlelist = response.xpath('//title/text()').extract()

		for line in titlelist:
			title = line.encode('utf-8')
			item['title'] += title

		timelist = response.xpath("//*/div[@class='c_subtitle']//text()").extract_first()
		if timelist is None:
			item['time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
		else:
			i=0
			while(i<=18):
				timelist = response.xpath("//*/div[@class='c_subtitle']//text()").extract_first()[i + 18]
				if timelist=='-' or timelist==' ' or timelist==':':
					item['time'] += '_'
				else:
					item['time'] += timelist
				i+=1

		contentlist = response.xpath("//*/div[@class='c_show_content']//text()").extract()
		for con in contentlist:
			content = con.encode('utf-8')
			item['content'] += content

		yield item


