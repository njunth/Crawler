# -*- coding: utf-8 -*-

# Scrapy settings for tianyav2 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import os;

BOT_NAME = 'tianyav2'

SPIDER_MODULES = ['base.spiders.tianya']
NEWSPIDER_MODULE = 'base.spiders.tianya'

LOG_LEVEL = 'INFO'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tianyav2 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 2

COOKIES_ENABLED = False

DOWNLOAD_TIMEOUT = 20

RETRY_ENABLED = False



# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'tianyav2.middlewares.Tianyav2SpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'tianyav2.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# DOWNLOADER_MIDDLEWARES = {
#          'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
#          # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
#          # 'base.downloaders.retry.RetryMiddleware': 500,
#          'base.downloaders.proxy_middlewares.ProxyMiddleware':100
#     }


# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'base.pipelines.tianya.pipelines.Tianyav2Pipeline': 300,
}
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")  # 主机IP
MONGO_PORT = (int)(os.getenv("MONGO_PORT", 27017))  # 端口号
MONGODB_DBNAME = os.getenv("MONGO_DBNAME", "Crawler")  # 库名
MONGODB_COLLECTION = "Tianyaluntan"  # collection名

#LOG_LEVEL = 'INFO'
# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
