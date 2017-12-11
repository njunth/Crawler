import scrapy

from base.items.qihang.items import QihangItem
from scrapy.http import Request
import datetime
from base.items.qihang.BloomFilter import BloomFilter

class spider(scrapy.Spider):
	name="spider"
	allowed_domains=["www.qihang.com.cn"]

	start_urls=["http://www.qihang.com.cn"]

	def parse(self,response):
		self.bf=BloomFilter(0.0001,1000000)
		while 1:
			urls = response.xpath("//*/a/@href").extract()
			for url in urls:
				urlc = 'http://www.qihang.com.cn'
				for urllist in url:
					urll = urllist.encode('utf-8')
					urlc += urll
				if(self.bf.is_element_exist(urlc)==False):
					yield Request(urlc,callback=self.parse_inPage)
				else:
					continue


	def parse_inPage(self,response):

		item=QihangItem()
		item['title'] = ''
		item['source'] = "QiHangKaoYan"
		item['source_url'] = "http://www.qihang.com.cn/"
		item['url'] = response.url
		item['html'] = ''
		item['time'] = ''
		item['content'] = ''
		item['attention'] = 0
		item['sentiment'] = 0
		item['create_time']= datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
		contentlist = response.xpath("//html").extract()

		self.bf.insert_element(response.url)

		for con in contentlist:
			utfcontent = con.encode('utf-8')
			item['html'] += utfcontent
		titlelist = response.xpath('//title/text()').extract()

		for line in titlelist:
			title = line.encode('utf-8')
			item['title'] += title

		timelist = response.xpath("//li[@class='content_lt21']/text()").extract_first()
		if timelist is None:
			item['time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
		else:
			i=0
			while (i <= 9):
				timelist = response.xpath("//li[@class='content_lt21']//text()").extract_first()[i+5]
				if timelist=='-' or timelist==' ' or timelist==':' :
					item['time']+= '_'
				else:
					item['time']+=timelist.encode('utf-8')
				i+=1
			item['time'] +="_00_00_00"


		contentlist = response.xpath("//div[@class='content_lt5']//text()").extract()
		for con in contentlist:
			content = con.encode('utf-8')
			item['content'] += content
		yield item

