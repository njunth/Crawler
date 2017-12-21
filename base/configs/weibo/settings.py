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

MONGO_HOST = os.getenv("MONGO_HOST", "114.212.189.147")
MONGO_PORT = (int)(os.getenv("MONGO_PORT", 10100))
MONGODB_DBNAME = os.getenv("MONGO_DBNAME", "Crawler")
MONGODB_COLLECTION = 'Weibo'

MYSQL_HOST = os.getenv("MYSQL_HOST", "114.212.189.147")
MYSQL_PORT = (int)(os.getenv("MYSQL_PORT", 10103))
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "woodpecker")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "crawl_nju903")
MYSQL_TABLE = 'keyword_t'

LOG_LEVEL = 'INFO'

# IPPOOL=[
#     "120.198.224.5:8080",
#     "120.198.224.110:8080",
#     "120.198.224.5:90",
#     "120.198.224.7:8080",
#     "120.198.224.5:8000",
#     "120.198.224.5:8088",
#     "120.198.224.101:8080",
#     "120.198.224.103:8080",
#     "120.198.224.102:8088",
#     "120.192.222.26:63000",
#     "120.198.224.7:8088",
#     "112.80.224.13:8888",
#     "47.100.14.11:8080",
#     "120.198.224.102:8080",
#     "39.91.33.121:8118",
#     "101.4.136.34:81",
#     "120.198.224.105:8080",
#     "118.114.77.47:8080",
#     "120.198.224.5:80",
#     "120.198.224.6:8080",
#     "120.198.224.6:80",
#     "218.201.98.196:3128",
#     "182.61.117.113:80",
#     "59.41.202.6:53281",
#     "123.176.103.44:80",
#     "121.207.0.153:808",
#     "61.153.67.110:9999",
#     "120.198.224.108:8080",
#     "120.198.224.106:8080",
#     "120.198.224.107:8080",
#     "222.73.68.144:8090",
#     "103.233.168.9:53005",
#     "124.42.7.103:80",
#     "101.132.141.133:3128",
#     "120.198.224.104:8080",
#     "120.198.224.109:8080",
#     "114.215.102.168:8081",
#     "119.23.141.97:9000",
#     "27.184.137.102:8888",
#     "120.198.224.109:8088",
#     "61.135.155.82:443",
#     "106.14.12.240:8082",
#     "222.186.32.227:8118",
#     "123.56.109.24:808",
#     "175.5.44.79:808",
#     "39.155.169.70:80",
#     "219.142.188.203:8888",
#     "121.226.153.197:808",
#     "60.177.228.98:808",
#     "60.168.80.199:808",
#     "182.34.101.143:808",
#     "171.217.35.4:808",
#     "120.34.42.40:808",
#     "113.67.183.248:8118",
#     "112.114.98.103:8118",
#     "112.114.96.56:8118",
#     "183.12.27.45:8118",
#     "112.114.98.143:8118",
#     "123.152.76.238:8118",
#     "110.73.49.139:8123",
#     "139.196.17.196:8118",
#     "112.114.96.237:8118",
#     "180.110.248.182:8118",
#     "121.196.226.246:84",
#     "114.215.103.121:8081",
#     "112.114.96.195:8118",
#     "60.255.186.169:8888",
#     "120.55.61.182:80",
#     "101.200.55.71:8080",
#     "112.114.99.218:8118",
#     "115.204.120.177:808",
#     "183.144.207.47:3128",
#     "125.86.58.151:8118",
#     "60.162.19.33:808",
#     "182.38.120.79:808",
#     "223.242.131.76:52424",
#     "219.138.58.247:3128",
#     "180.155.129.3:45403",
#     "112.114.93.242:8118",
#     "112.114.99.130:8118",
#     "120.198.224.6:8000",
#     "120.198.224.7:80",
#     "58.250.168.164:9000",
#     "58.56.128.84:9001",
#     "42.84.176.141:53281",
#     "118.193.26.18:8080",
#     "114.215.30.108:8118",
#     "180.156.95.61:8118",
#     "112.114.93.4:8118",
#     "112.114.97.166:8118",
#     "112.114.96.96:8118",
#     "101.205.87.106:808",
#     "116.62.170.104:3128",
#     "112.114.94.106:8118",
#     "117.43.0.242:808",
#     "124.232.163.4:3128",
#     "219.138.58.235:3128",
#     "139.196.13.42:80"]
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
DOWNLOADER_MIDDLEWARES = {
         'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
         'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
         'base.downloaders.weibo_retry.RetryMiddleware': 500,
         'base.downloaders.weibo_proxy_middlewares.ProxyMiddleware':100
    }

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

# DOWNLOADER_MIDDLEWARES = {
# #    'myproxies.middlewares.MyCustomDownloaderMiddleware': 543,
#      'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware':543,
#      'base.downloaders.weibo.middlewares.MyproxiesSpiderMiddleware':125
# }

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
