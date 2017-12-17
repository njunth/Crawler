# coding=utf-8
import scrapy

from base.items.kaicheng.items import KaichengItem
from scrapy.http import Request
import datetime, random, time
from base.items.kaicheng.BloomFilter import BloomFilter

class spider(scrapy.Spider):
	name="spider"
	allowed_domains=["www.kaichengschool.com"]

	start_urls=["http://www.kaichengschool.com"]


	def parse(self,response):
		self.bf=BloomFilter(0.0001, 1000000)
		while 1:
			urls = response.xpath("//*/a/@href").extract()
			for url in urls:
				urlc = 'http://www.kaichengschool.com'
				for urllist in url:
					urll = urllist.encode('utf-8')
					urlc += urll
				if(self.bf.is_element_exist(urlc)==False):
					yield Request(urlc,callback=self.parse_inPage)
				else:
					continue
			yield Request( "http://www.kaichengschool.com", callback=self.parse )


	def parse_inPage(self,response):
		sleep_time = random.random()
		print sleep_time
		time.sleep( sleep_time )
		item=KaichengItem()
		item['title'] = ''
		item['source'] = "凯程考研"
		item['source_url'] = "http://www.kaichengschool.com"
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

		timelist = response.xpath("//div[@class='label']/p/text()").extract_first()
		if timelist is None:
			item['time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
		else:
			timelist=response.xpath("//div[@class='label']/p/text()").extract_first()[3]
			if timelist!='2':
				item['time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
			else:
				i=0
				while (i <= 16):
					timelist = response.xpath("//div[@class='label']/p/text()").extract_first()[i+3]
					if timelist=='-' or timelist==' ' or timelist==':' or timelist==',':
						item['time']+= '_'
					else:
						item['time']+=timelist.encode('utf-8')
					i+=1
				item['time']+='00'


		contentlist = response.xpath("//div[@class='conrents-c']//text()").extract()
		for con in contentlist:
			content = con.encode('utf-8')
			item['content'] += content
		yield item

		urls = response.xpath("//*/a/@href").extract()
		for url in urls:
			urlc = 'http://www.kaichengschool.com'
			for urllist in url:
				urll = urllist.encode('utf-8')
				urlc += urll
			if(self.bf.is_element_exist(urlc)==False):
				yield Request(urlc, callback=self.parse_inPage)

			else:
				continue

