import scrapy

from base.items.xindongfang.items import XinItem
# from scrapy.selector import Selector
from scrapy.http import Request
import datetime
# from scrapy.spider import Spider
from base.items.xindongfang.BloomFilter import BloomFilter

class spider(scrapy.Spider):
	name="spider"
	allowed_domains=["kaoyan.koolearn.com"]

	start_urls=["http://kaoyan.koolearn.com"]

#	def start_requests(self):
	def parse(self,response):
		self.bf=BloomFilter(0.0001,1000000)
		url = response.url
		yield Request(url,callback=self.parse_inPage)
		urls = response.xpath("//li/a/@href|//div/a/@href|//td/a/@href").extract()
		for url in urls:
			if(self.bf.is_element_exist(url)==False):
				yield Request(url,callback=self.parse_inPage)
			else:
				continue

#		urls = response.xpath("//div/a/@href").extract()
#		for url in urls:
#			yield Request(url,callback=self.parse_inPage)


	def parse_inPage(self,response):
        ##	sel=Selector(response)
        ##	site=sel
        #		url="http://kaoyan.koolearn.com"

		item=XinItem()
		item['title']=''
		item['source']="XingDongFangKaoYan"
		item['source_url']="http://kaoyan.koolearn.com"
		item['url']=response.url
		item['html']=''
		item['time']=''
		item['content']=''
		item['attention']=0
		item['sentiment']=0
		contentlist=response.xpath('//html').extract()
        
		self.bf.insert_element(response.url)

#		contentlist=response.xpath("//a/@href").extract()
		for con in contentlist:
			utfcontent=con.encode('utf-8')
			item['html']+=utfcontent
		titlelist=response.xpath('//title/text()').extract()
#		item['title']+=response.xpath('//title/text()').extract()

#		for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
#			url = response.urljoin(response.url,href.extract())


		for line in titlelist:
			title=line.encode('utf-8')
			item['title']+=title
# 			item['title']+='\n'

		# timelist = response.xpath("//i[@class='s_tit_i1']/text()").extract()
		# print timelist
		#for times in timelist:
		timelist = response.xpath( "//i[@class='s_tit_i1']/text()" ).extract_first()
		# print timelist
		if timelist is None:
			item['time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
		else:
			i = 0
			while(i<=18):
				if i!=4 and i!=7 and i!=10 and i!=13 and i!=16:
					#time = times.encode('utf-8')
					timelist = response.xpath("//i[@class='s_tit_i1']/text()").extract_first()[i]
					item['time'] += timelist
				else:
					item['time']+='_'
				i+=1
		# print item['time']

		#contentlist = response.xpath("//div[@class='mt40']/p/*/text()|//div[@class='mt40']/p/text()|//div[@class='mt40']/p/*/*/text()").extract()
		contentlist = response.xpath("//div[@class='mt40']//text()").extract()
		for con in contentlist:
			content = con.encode('utf-8')
			item['content'] += content


		yield item
#		yield Request(url,callback=self.parse)

