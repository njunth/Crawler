# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import scrapy
import requests
from scrapy import signals, log
import base64
from base.configs.settings import PROXY_SERVICE_ADDRESS
import random

class ProxyMiddleware(object):

    def __init__(self, ip=''):
        self.ip = ip
    # def __init__(self):
        # self.proxy = DEFAULT_PROXY
        # self.proxy_use = 0
        # self.max_use = int(PROXY_MAX_USE)
        # self.proxy = self.update_proxy()

    # def update_proxy(self):
    #     return "bh21.84684.net:21026"
        # service_address = PROXY_SERVICE_ADDRESS+'get/'
        # # print service_address
        # try:
        #     response = requests.get(service_address, timeout=5)
        #     # print response.status_code
        #     if response.status_code == 200:
        #         return response.text
        #     return self.proxy
        # except:
        #     print " failed get service_address"
        #     return self.proxy

    def process_request(self, request, spider):
        service_address = PROXY_SERVICE_ADDRESS
        # print service_address
        try:
            response = requests.get(service_address, timeout=10)
            # print response.status_code
            if response.status_code == 200:
                proxy = response.text
                request.meta['proxy'] = 'http://' + proxy
        except:
            request.meta['proxy'] = 'http://127.0.0.1:9743'
            print " failed get new service_address"

        # proxy_user_pass = "dailaoshi:D9xvyfrgPwqBx39u"
        # encoded_user_pass = base64.encodestring( proxy_user_pass )
        # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        print request.meta['proxy']
        # if request.meta.get('change_proxy', False):
        #     self.proxy = self.update_proxy()
        #     msg = 'ProxyMiddleware: Change proxy to:' + self.proxy
        #     log.msg(msg, level=log.INFO)
        #     request.meta['change_proxy'] = False
        # request.meta['proxy'] = 'http://'+self.proxy
        # print request.meta['proxy']
        # self.proxy_use += 1
        # if self.proxy_use > self.max_use:
        #     self.proxy_use = 0
        #     self.proxy = self.update_proxy()
        #     msg = 'Change proxy to:' + self.proxy
        #     log.msg(msg, level=log.INFO)
        return None
        # request.meta['proxy'] = 'http://110.206.127.136:9797'
