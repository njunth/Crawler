# coding=utf-8
import scrapy

from base.items.xindongfang.items import XinItem
from scrapy.http import Request
import datetime, random, time
from base.items.xindongfang.BloomFilter import BloomFilter

class spider(scrapy.Spider):
	name="spider"
	allowed_domains=["kaoyan.koolearn.com"]

	start_urls=["http://kaoyan.koolearn.com"]

	def parse(self,response):
		self.bf=BloomFilter(0.0001,1000000)
		while 1:
			urls = response.xpath("//li/a/@href|//div/a/@href|//td/a/@href").extract()
			for url in urls:
				if(self.bf.is_element_exist(url)==False):
					yield Request(url,callback=self.parse_inPage, dont_filter=True)
				else:
					continue

	def parse_inPage(self,response):
		sleep_time = random.random()
		print sleep_time
		time.sleep( sleep_time )
		item=XinItem()
		item['title']=''
		item['source']="新东方"
		item['source_url']="http://kaoyan.koolearn.com"
		item['url']=response.url
		item['html']=''
		item['time']=''
		item['content']=''
		item['attention']=0
		item['sentiment']=0
		item['create_time']= datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
		contentlist=response.xpath('//html').extract()
        
		self.bf.insert_element(response.url)

		for con in contentlist:
			utfcontent=con.encode('utf-8')
			item['html']+=utfcontent
		titlelist=response.xpath('//title/text()').extract()


		for line in titlelist:
			title=line.encode('utf-8')
			item['title']+=title

		timelist = response.xpath( "//i[@class='s_tit_i1']/text()" ).extract_first()
		if timelist is None:
			item['time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
		else:
			i = 0
			while(i<=18):
				if i!=4 and i!=7 and i!=10 and i!=13 and i!=16:
					timelist = response.xpath("//i[@class='s_tit_i1']/text()").extract_first()[i]
					item['time'] += timelist
				else:
					item['time']+='_'
				i+=1

		contentlist = response.xpath("//div[@class='mt40']//text()").extract()
		for con in contentlist:
			content = con.encode('utf-8')
			item['content'] += content


		yield item


