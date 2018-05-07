# -*- coding: utf-8 -*-
# proxy settings
import os;

# PROXY_SERVICE_ADDRESS = os.getenv("PROXY_SERVICE_ADDRESS", "http://114.212.189.147:10102/")
PROXY_SERVICE_ADDRESS = os.getenv("PROXY_SERVICE_ADDRESS", "http://114.212.189.147:10096/")
PROXY_MAX_USE = '30'
DEFAULT_PROXY = '113.108.204.74:8888'

IP_SERVER = '125.121.136.247:31730'
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")  # 主机IP
REDIS_PORT = (int)(os.getenv("REDIS_PORT", 6379))  # 端口号


