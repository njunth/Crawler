#encoding=utf-8
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from base.items.baidutiebaquanbasousuo.items import BaidutiebaquanbasousuoItem
from base.items.baidutiebaquanbasousuo.bloomfliter import BloomFilter
from datetime import datetime
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class BaidutiebaquanbasousuoSpider(Spider):
    name = 'spider'
    allowed_domains=["tieba.baidu.com"]


    def __init__(self, name=None, **kwargs):

        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []
        self.mainpage="http://www.csbiji.com/forum.php"


    def start_requests(self):
        keywords = ['出售', '提供', '发现', '高考', '考研', '研考', '硕士考试', '硕士生考试', '成考', '成人高考', '自考', '自学考试']
        url_p1 = 'http://tieba.baidu.com/f/search/res?isnew=1&kw=&qw='
        url_p2 = '&rn=10&un=&only_thread=0&sm=1&sd=&ed=&pn='
        while 1:
            for keyword in keywords:
                key = urllib.quote(keyword)
                for i in range(1, 200):
                    url = url_p1 + key + url_p2 + str(i)
                    yield Request(url=url,callback=self.parse_mainPage)

    def parse_inPage(self,response):
        url = response.url
        item =BaidutiebaquanbasousuoItem()
        #contains(@class , 'ico-tag')
        content_div1 = response.selector.xpath('//div[@class="d_post_content_main d_post_content_firstfloor"]')
        content_div2 = response.selector.xpath('//div[@class="d_post_content_main"] | //div[@class="d_post_content_main "]')
        #content_div2 = response.selector.xpath('//div[contains(@class,"d_post_content_main")]|//div[contains(@class,"d_post_content_main ")]')
        content1=content_div1.xpath('string(.)').extract()
        content2=content_div2.xpath('string(.)').extract()
        content1.extend(content2)
        try:
            if (len(content1)>0):
                item['source']='Baidutieba'
                item['source_url']='https://tieba.baidu.com/index.html'
                item['url']=url
                item['html']=response.body
                item['n_click']=0
                item['n_reply']=len(content1)-1
                item['content'] = content1
                item['title'] = response.selector.xpath("//title/text()").extract()[0]
                item['attention'] = 0
                text=str(response.body)
                time_str=re.findall(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}',text)
                item['time']=time_str
                authid_str=response.selector.xpath("//li[@class='d_name']")
                authid_str2=authid_str.xpath('string(.)').extract()
                item['authid']=authid_str2
                item['sentiment']=0
                item['create_time']=str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
                yield item
        except:
            print('error')

    def parse_mainPage(self,response):
        sel=Selector(response)
        sites=sel.xpath("//a[@data-tid and @data-fid]/@href").extract()
        for t in sites:
            print t
        for site in sites:
            if not site.startswith('http'):
                urls = "http://tieba.baidu.com"+site
            else:
                urls=site
            print urls
            yield Request(urls,callback=self.parse_inPage)
