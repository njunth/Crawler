# coding=utf-8
import scrapy

from base.items.zhuoyue.items import ZhuoyueItem
from scrapy.http import Request
import datetime, random, time
from base.items.zhuoyue.BloomFilter import BloomFilter
# from base.items.Bloomfilter import BloomFilter

class spider(scrapy.Spider):
	name="spider"
	allowed_domains=["www.zhuoyuekaoyan.com"]

	start_urls=["http://www.zhuoyuekaoyan.com"]
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
	}


	def parse(self,response):
		self.bf = BloomFilter(0.0001,100000)
		while 1:
			urls = response.xpath("//*/a/@href").extract()
			for url in urls:
				urlc = 'http://www.zhuoyuekaoyan.com'
				if not url.startswith('http'):
					for urllist in url:
						urll = urllist.encode('utf-8')
						urlc += urll
				# print urlc
				if(self.bf.is_element_exist(urlc)==False):
					yield Request(urlc,callback=self.parse_inPage, dont_filter=True)
				else:
					continue
				sleep_time = random.random()
				print sleep_time
				time.sleep( sleep_time )
			yield Request("http://www.zhuoyuekaoyan.com", callback=self.parse, dont_filter=True)


	def parse_inPage(self,response):
		item=ZhuoyueItem()
		item['title'] = ''
		item['source'] = "卓越考研"
		item['source_url'] = "http://www.zhuoyuekaoyan.com"
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

		timelist = response.xpath("//div[@class='detail-subtitle']/span/text()").extract_first()
		if timelist is None:
			item['time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
		else:
			i = 0
			while (i <= 15):
				timelist = response.xpath("//div[@class='detail-subtitle']/span/text()").extract_first()[i + 5]
				if timelist == '-' or timelist == ' ' or timelist == ':':
					item['time'] += '_'
				else:
					item['time'] += timelist.encode('utf-8')
				i += 1
			item['time'] += '_00'


		contentlist = response.xpath("//div[@class='detail-main']//text()").extract()
		for con in contentlist:
			content = con.encode('utf-8')
			item['content'] += content
		yield item

		urls = response.xpath("//*/a/@href").extract()
		for url in urls:
			urlc = 'http://www.zhuoyuekaoyan.com'
			for urllist in url:
				urll = urllist.encode('utf-8')
				urlc += urll
			if(self.bf.is_element_exist(urlc)==False):
				yield Request(urlc, callback=self.parse_inPage, dont_filter=True)

			else:
				continue

