# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()
    n_forword = scrapy.Field()
    n_comment = scrapy.Field()
    n_like = scrapy.Field()
    attention = scrapy.Field()
    sentiment = scrapy.Field()
    keyword = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()
    publisher=scrapy.Field()
    pass
