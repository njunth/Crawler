# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WenduItem(scrapy.Item):
    source = scrapy.Field()
    source_url = scrapy.Field()
    url = scrapy.Field()
    html = scrapy.Field()
    attention = scrapy.Field()
    content = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    sentiment = scrapy.Field()
    create_time=scrapy.Field()
    pass
