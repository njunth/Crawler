# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    html = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()
    source_url = scrapy.Field()
    time = scrapy.Field()
    attention = scrapy.Field()
    sentiment = scrapy.Field()
    pass
