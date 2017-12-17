# coding=utf-8
import scrapy
from base.items.tianya.items import Tianyav2Item
from base.items.tianya.BloomFilter import BloomFilter
import re
import datetime, random, time



class Tianyaspider(scrapy.Spider):
    name =  "spider"

    allowed_domins = ["tianya.cn"]

    start_urls = {
        "http://bbs.tianya.cn/"
        #"http://bbs.tianya.cn/post-travel-821028-1.shtml"
    }

    #bf = BloomFilter(0.1, 10)

    def parse(self,response):

        #item = Tianyav2Item()
        #self.bf = BloomFilter(0.0001, 1000000)
        while 1:
            for url1 in response.selector.xpath("//li/div[@class='title']/a/@href").re(r'^http://bbs.tianya.*'):
                #if (self.bf.is_element_exist(url1) == False):  # reduce a /
                yield scrapy.Request(url=url1, callback=self.parse_inpage)
                #else:
                    #continue
            yield scrapy.Request(url="http://bbs.tianya.cn/", callback=self.parse)

    def parse_inpage(self,response):
        sleep_time = random.random()
        print sleep_time
        time.sleep( sleep_time )
        item = Tianyav2Item()
        content = response.selector.xpath('//div[@class="atl-main"]//div/div[@class="atl-content"]/div[2]/div[1]')#/text()').extract()
        con_div = content.xpath('string(.)').extract()

        if re.match('^http://bbs.tianya.*.shtml', response.url) and len(con_div)>0:
            item['source'] = "天涯论坛"
            item['source_url'] = 'http://bbs.tianya.cn/'
            """try:
                item['html'] = response.body.decode('gbk')
            except:
                item['html'] = response.body"""

            item['html'] = ''
            contentlist = response.xpath('//html').extract()
            for con in contentlist:
                utfcontent = con.encode('utf-8')
                item['html'] += utfcontent

            item['url'] = response.url

            #item['title'] = response.xpath('//*[@id="post_head"]/h1/span[1]/span/text()').extract()[0].encode('utf-8')
            t = response.xpath('//*[@id="post_head"]/h1/span[1]/span/text()').extract()#[0].encode('utf-8')
            title = ''.join(t)
            title1 = title.encode('utf-8')
            item['title'] = title1

            # collection名
            temp = response.xpath('//div[@class="atl-info"]/span[2]/text()').extract_first()
            time_collection = []

            if temp is not None:
                tc = response.xpath('//div[@class="atl-info"]/span[2]/text()').extract_first()[3]
                time_collection.append(tc)
                tc = response.xpath('//div[@class="atl-info"]/span[2]/text()').extract_first()[4]
                time_collection.append(tc)
                tc = response.xpath('//div[@class="atl-info"]/span[2]/text()').extract_first()[5]
                time_collection.append(tc)
                tc = response.xpath('//div[@class="atl-info"]/span[2]/text()').extract_first()[6]
                time_collection.append(tc)

                time_collection.append('_')

                tc = response.xpath('//div[@class="atl-info"]/span[2]/text()').extract_first()[8]
                time_collection.append(tc)
                tc = response.xpath('//div[@class="atl-info"]/span[2]/text()').extract_first()[9]
                time_collection.append(tc)
                time_collection.append('_')
                tc = response.xpath('//div[@class="atl-info"]/span[2]/text()').extract_first()[11]
                time_collection.append(tc)
                tc = response.xpath('//div[@class="atl-info"]/span[2]/text()').extract_first()[12]
                time_collection.append(tc)

                time_collection.append('_')
            # time = []
                article_time = response.xpath('//div[@class="atl-info"]/span[2]/text()').extract_first()[14]
                time_collection.append(article_time)
                article_time = response.xpath('//div[@class="atl-info"]/span[2]/text()').extract_first()[15]
                time_collection.append(article_time)

                time_collection.append('_')

                article_time = response.xpath('//div[@class="atl-info"]/span[2]/text()').extract_first()[17]
                time_collection.append(article_time)
                article_time = response.xpath('//div[@class="atl-info"]/span[2]/text()').extract_first()[18]
                time_collection.append(article_time)
                time_collection.append('_')
                article_time = response.xpath('//div[@class="atl-info"]/span[2]/text()').extract_first()[20]
                time_collection.append(article_time)
                article_time = response.xpath('//div[@class="atl-info"]/span[2]/text()').extract_first()[21]
                time_collection.append(article_time)
                item['time'] = ''.join(time_collection)
            else:
                item['time'] = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

            # collection_name = ''.join(time_collection)
            # tianyav2.config.set_name(collection_name)

            item['authid'] = response.xpath('//div[@class="atl-info"]/span[1]/a/text()').extract()#.re(r'[0-9]*')
            item['testtime'] = response.xpath('//div[@class="atl-info"]/span[2]/text()').extract()

            # article_content = response.xpath('//div[@class="atl-main"]//div/div[@class="atl-content"]/div[2]/div[1]/text()').extract()#[0].encode('utf-8')
            #item['content'] = response.xpath(
                #'//div[@class="atl-main"]//div/div[@class="atl-content"]/div[2]/div[1]/text()').extract()
            #item['content'] = ''.join(item['content'])
            item['content'] = con_div

            click = response.xpath('//div[@class="atl-info"]/span[3]/text()').re(r'[0-9]*')
            if click is None:
                item['n_click'] = 0
            else:
                clickstr = ''.join(click)
                if clickstr is '':
                    item['n_click'] = 0
                else:
                    item['n_click'] = int(clickstr)

            reply = response.xpath('//div[@class="atl-info"]/span[4]/text()').re(r'[0-9]*')
            if reply is None:
                item['n_reply'] = 0
            else:
                replystr = ''.join(reply)
                if replystr is '':
                    item['n_reply'] = 0
                else:
                    item['n_reply'] = int(replystr)

            item['sentiment'] = 0
            item['attention'] = 0

            #self.bf.insert_element(response.url)

            yield item


