import scrapy

from base.items.zhonggong.items import ZhonggongItem
from scrapy.http import Request
import datetime, random, time
from base.items.zhonggong.BloomFilter import BloomFilter

class spider(scrapy.Spider):
	name="spider"
	allowed_domains=["www.kaoyan365.cn"]

	start_urls=["http://www.kaoyan365.cn/"]

	def parse(self,response):
		self.bf=BloomFilter(0.0001,1000000)
		while 1:
			urls = response.xpath("//div[@class='offcn_index_m1_center fl']//a[starts-with(@href,'http')]/@href   |  //div[@class='offcn_m2_right fr']//a[starts-with(@href,'http')]/@href   |   //div[@class='offcn_main3 offcn_mt20 layout']//*/a[starts-with(@href,'http')]/@href   |   //div[@class='offcn_main4 layout']//a[starts-with(@href,'http')]/@href   |   //div[@class='offcn_main7 offcn_mt20 layout']//a[starts-with(@href,'http')]/@href").extract()
			for url in urls:
				if(self.bf.is_element_exist(url)==False):
					yield Request(url,callback=self.parse_inPage)
				else:
					continue


	def parse_inPage(self,response):
		sleep_time = random.random()
		print sleep_time
		time.sleep( sleep_time )
		item=ZhonggongItem()
		item['title'] = ''
		item['source'] = "ZhongGongKaoYan"
		item['source_url'] = "http://www.kaoyan365.cn/"
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

		timelist = response.xpath("//div[@class='offcn_show_ly']/font[2]/text()").extract_first()
		if timelist is None:
			item['time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
		else:
			j=0
			while(j<=23):
				timelist = response.xpath("//div[@class='offcn_show_ly']/font[2]/text()").extract_first()[j]
				if timelist=='2':
					break
				j+=1
			i=0
			while (i <= 18):
				timelist = response.xpath("//div[@class='offcn_show_ly']/font[2]/text()").extract_first()[i+j]
				if timelist=='-' or timelist==' ' or timelist==':' :
					item['time']+= '_'
				else:
					item['time']+=timelist.encode('utf-8')
				i+=1


		contentlist = response.xpath("//div[@class='offcn_show_cont_02']//text()").extract()
		for con in contentlist:
			content = con.encode('utf-8')
			item['content'] += content
		yield item

