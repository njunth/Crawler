import scrapy

from base.items.haiwen.items import HaiwenItem
from scrapy.http import Request
import datetime, random, time
from base.items.haiwen.BloomFilter import BloomFilter

class spider(scrapy.Spider):
	name="spider"
	allowed_domains=["kaoyan.wanxue.cn"]

	start_urls=["http://kaoyan.wanxue.cn"]

	def parse(self,response):
		self.bf=BloomFilter(0.0001,1000000)
		while 1:
			urls = response.xpath("//ul[@class='con_l']//a[starts-with(@href,'http')]/@href  |  //ul[@class='con_r']//a[starts-with(@href,'http')]/@href   |   //div[@class='tab_box']//a[starts-with(@href,'http')]/@href").extract()
			for url in urls:
				if(self.bf.is_element_exist(url)==False):
					yield Request(url,callback=self.parse_inPage)
				else:
					continue



	def parse_inPage(self,response):
		sleep_time = random.random()
		print sleep_time
		time.sleep( sleep_time )
		item=HaiwenItem()
		item['title']=''
		item['source']="海文考研"
		item['source_url']="http://kaoyan.wanxue.cn"
		item['url']=response.url
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

		timelist = response.xpath("//div[@class='information_details_title pb25']/span/text()").extract_first()
		if timelist is None:
			item['time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
		else:
			i=0
			while (i <= 18):
				timelist = response.xpath("//div[@class='information_details_title pb25']/span/text()").extract_first()[i]
				if timelist == '-' or timelist == ' ' or timelist == ':':
					item['time'] += '_'
				else:
					item['time'] += timelist.encode('utf-8')
				i += 1

		contentlist = response.xpath("//div[@class='information_details_content']//text()").extract()
		for con in contentlist:
			content = con.encode('utf-8')
			item['content'] += content
		yield item

