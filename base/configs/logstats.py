import logging

import datetime
from twisted.internet import task

from scrapy.exceptions import NotConfigured
from scrapy import signals

logger = logging.getLogger(__name__)


class LogStats(object):
    """Log basic scraping stats periodically"""

    def __init__(self, stats, interval=60.0):
        self.stats = stats
        self.interval = interval
        self.multiplier = 60.0 / self.interval
        self.task = None

    @classmethod
    def from_crawler(cls, crawler):
        interval = crawler.settings.getfloat('LOGSTATS_INTERVAL')
        if not interval:
            raise NotConfigured
        o = cls(crawler.stats, interval)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_opened(self, spider):
        self.pagesprev = 0
        self.itemsprev = 0

        self.item_insert = 0.


        self.task = task.LoopingCall(self.log, spider)
        self.task.start(self.interval)


    def log(self, spider):
        items = self.stats.get_value('item_scraped_count', 0)
        pages = self.stats.get_value('response_received_count', 0)
        items_insert = self.stats.get_value('item_insert_count', 0)
        irate = (items - self.itemsprev) * self.multiplier
        prate = (pages - self.pagesprev) * self.multiplier
        insert_rate = (items_insert - self.item_insert) * self.multiplier
        self.pagesprev, self.itemsprev = pages, items
        self.item_insert = items_insert

        print datetime.datetime.now().strftime( '%Y_%m_%d_%H_%M_%S' ),

        # print items, pages

        print "Crawled {} pages (at {} pages/min),scraped {} items (at {} items/min)".format(pages,prate,items_insert,insert_rate)

        # msg = ("Crawled %(pages)d pages (at %(pagerate)d pages/min), "
        #        "scraped %(items)d items (at %(itemrate)d items/min)")
        # log_args = {'pages': pages, 'pagerate': prate,
        #             'items': items, 'itemrate': irate}
        # print logger.info(msg, log_args, extra={'spider': spider})

    def spider_closed(self, spider, reason):
        if self.task and self.task.running:
            self.task.stop()
