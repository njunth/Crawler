# -*- coding: utf-8 -*-

# Scrapy settings for scrapy_google project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import os

BOT_NAME = 'google'

SPIDER_MODULES = ['base.spiders.google']
NEWSPIDER_MODULE = 'base.spiders.google'

MONGODB_HOST = os.getenv("MONGO_HOST", "114.212.189.147")
MONGODB_PORT = (int)(os.getenv("MONGO_PORT", 10100))
MONGODB_DBNAME = os.getenv("MONGO_DBNAME", "Crawler")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "google")
# MONGO_HOST = "localhost"
# MONGO_PORT = 27017
# MONGODB_DBNAME = 'Crawler'
# MONGODB_COLLECTION = 'google'
MYSQL_HOST = os.getenv("MYSQL_HOST", "114.212.189.147")
MYSQL_PORT = (int)(os.getenv("MYSQL_PORT", 10136))
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "woodpecker")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "crawl_nju903")
MYSQL_TABLE = 'keyword_t'
SPIDER_COUNTS = (int)(os.getenv("SPIDER_COUNTS", 10))
KEYWORD_INDEX = (int)(os.getenv("KEYWORD_INDEX", 0))

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapy_google (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# LOG_ENABLED = False

EXTENSIONS = {
    'scrapy.extensions.logstats.LogStats': None,
    'base.configs.logstats.LogStats': 150,
}

# DOWNLOADER_MIDDLEWARES = {
#          'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#          'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
#          # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
#          # 'base.downloaders.retry.RetryMiddleware': 500,
#          # 'base.downloaders.baidutiebaquanbasousuo.middlewares.MyUserAgentMiddleware': 400,
#          'base.downloaders.proxy_middlewares.ProxyMiddleware':100
#     }

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
#    'scrapy_google.middlewares.ScrapyGoogleSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'scrapy_google.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'base.pipelines.google.pipelines.ScrapyGooglePipeline': 300,
}

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
