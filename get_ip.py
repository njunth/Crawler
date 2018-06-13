import requests
from time import sleep
from base.configs.settings import PROXY_SERVICE_ADDRESS
from base.configs.weibo.settings import MONGO_HOST,MONGO_PORT
import pymongo


mongodbname = "Crawler"
collection_name = "ip_mongodb_name"
while 1:
    service_address = PROXY_SERVICE_ADDRESS
    # print service_address
    try:
        response = requests.get( service_address, timeout=10 )
        # print response.status_code
        if response.status_code == 200:
            proxy = response.text
            print "change ip:", proxy
            client = pymongo.MongoClient( MONGO_HOST, MONGO_PORT )
            db = client[mongodbname]
            collection = db[collection_name]
            collection.save( {
                '_id': "ip",
                'value': proxy
            } )
    except Exception, e:
        # request.meta['proxy'] = 'http://127.0.0.1:9743'
        print "failed get new service_address"
        print e
    sleep(0.5)