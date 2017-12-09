# -*- coding: utf-8 -*-

# Scrapy settings for weibo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import os
BOT_NAME = 'weibo'

SPIDER_MODULES = ['base.spiders.weibo']
NEWSPIDER_MODULE = 'base.spiders.weibo'

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = (int)(os.getenv("MONGO_PORT", 27017))
MONGODB_DBNAME = os.getenv("MONGO_DBNAME", "Crawler")
MONGODB_COLLECTION = 'Weibo'

LOG_LEVEL = 'INFO'

IPPOOL=["171.37.29.136:9797",
         "112.114.97.101:8118",
         "120.198.224.104:8080",
         "121.196.226.246:84",
         "120.198.224.7:80",
         "120.198.224.7:8080",
         "120.198.224.110:8080",
         "120.198.224.5:8080",
         "120.198.224.5:90",
         "120.198.224.109:8080",
         "101.132.141.133:3128",
         "120.198.224.5:8000",
         "120.198.224.5:8088",
         "114.215.102.168:8081",
         "120.198.224.101:8080",
         "114.215.103.121:8081",
         "120.198.224.103:8080",
         "58.250.168.164:9000",
         "123.133.52.247:81",
         "120.192.222.26:63000",
         "120.198.224.102:8088",
         "112.80.224.13:8888",
         "112.114.98.227:8118",
         "120.198.224.7:8088",
         "39.91.33.121:8118",
         "112.114.96.195:8118",
         "119.49.84.75:80",
         "47.100.14.11:8080",
         "120.198.224.102:8080",
         "120.35.12.105:3128",
         "101.4.136.34:81",
         "120.198.224.105:8080",
         "118.114.77.47:8080",
         "120.198.224.5:80",
         "120.198.224.6:8080",
         "110.73.9.168:8123",
         "119.23.141.97:9000",
         "112.114.96.239:8118",
         "171.35.103.37:808",
         "219.138.58.59:3128",
         "120.198.224.6:80",
         "120.77.182.248:80",
         "42.84.176.141:53281",
         "182.61.117.113:80",
         "27.184.137.102:8888",
         "218.201.98.196:3128",
         "60.255.186.169:8888",
         "110.216.67.211:80",
         "221.233.85.73:3128",
         "59.41.202.6:53281",
         "58.56.128.84:9001",
         "118.193.26.18:8080",
         "120.198.224.109:8088",
         "61.135.155.82:443",
         "103.251.36.123:8080",
         "123.176.103.44:80",
         "112.114.98.8:8118",
         "222.186.32.227:8118",
         "123.58.47.23:8080",
         "118.193.21.70:808",
         "121.207.0.153:808",
         "101.205.83.229:808",
         "115.46.75.90:8123",
         "106.14.12.240:8082",
         "114.246.176.192:8118",
         "112.114.92.144:8118",
         "101.200.55.71:8080",
         "120.55.61.182:80",
         "61.153.67.110:9999",
         "120.198.224.108:8080",
         "120.198.224.106:8080",
         "101.68.73.54:53281",
         "120.198.224.107:8080",
         "139.209.90.50:80",
         "123.56.109.24:808",
         "103.233.157.234:53281",
         "218.75.70.3:8118",
         "103.233.168.9:53005",
         "219.138.58.202:3128",
         "183.48.91.66:8118",
         "175.5.44.79:808",
         "114.215.30.108:8118",
         "222.73.68.144:8090"]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'weibo (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

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
#    'weibo.middlewares.WeiboSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'weibo.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'base.pipelines.weibo.pipelines.WeiboPipeline': 300,
}

DOWNLOADER_MIDDLEWARES = {
#    'myproxies.middlewares.MyCustomDownloaderMiddleware': 543,
     'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':543,
     'base.downloaders.weibo.middlewares.MyproxiesSpiderMiddleware':125
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
