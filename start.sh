#!/bin/bash

# SCRAPY_SETTINGS_MODULE=base.configs.wangyi_menhu.settings
# MONGO_HOST=114.212.189.147
# MONGO_PORT=10075
# MONGO_DBNAME=Crawler

docker run -e "SCRAPY_SETTINGS_MODULE=base.configs.wangyi_menhu.settings" -e "MONGO_HOST=114.212.189.147" -e "MONGO_PORT=10075" -e "MONGO_DBNAME=Crawler" -e "PYTHONPATH=/root/Crawler" -v /Users/lxs/workspace/Crawler:/root/Crawler -w=/root/Crawler registry.njuics.cn/library/scrapy scrapy crawl spider