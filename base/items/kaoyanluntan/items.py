# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KaoyanluntanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    source = scrapy.Field()
    source_url = scrapy.Field()
    url = scrapy.Field()
    html = scrapy.Field()
    n_click = scrapy.Field()
    n_reply = scrapy.Field()
    content = scrapy.Field()
    title = scrapy.Field()
    attention = scrapy.Field()
    time = scrapy.Field()
    sentiment = scrapy.Field()
    authid=scrapy.Field()
    create_time=scrapy.Field()
    pass
