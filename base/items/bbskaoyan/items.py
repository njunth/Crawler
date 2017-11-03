# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BbskaoyanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    origion = scrapy.Field()
    source_url =  scrapy.Field()
    current_url =  scrapy.Field()
    content = scrapy.Field()
    pass
