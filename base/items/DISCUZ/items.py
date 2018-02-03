# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DiscuzItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    source = scrapy.Field()
    source_url = scrapy.Field()
    url = scrapy.Field()
    html = scrapy.Field()
    n_click = scrapy.Field()
    attention = scrapy.Field()
    content = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    n_reply = scrapy.Field()
    sentiment = scrapy.Field()
    replies = scrapy.Field()
    authid = scrapy.Field()
    testtime = scrapy.Field()
    create_time = scrapy.Field()
