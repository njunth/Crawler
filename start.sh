#!/bin/bash

# SCRAPY_SETTINGS_MODULE=base.configs.wangyi_menhu.settings
# MONGO_HOST=114.212.189.147
# MONGO_PORT=10075
# MONGO_DBNAME=Crawler

docker run -e "SCRAPY_SETTINGS_MODULE=base.configs.wangyi_menhu.settings" -e "MONGO_HOST=114.212.189.147" -e "MONGO_PORT=10094" -e "MONGO_DBNAME=Crawler" -e "PYTHONPATH=/root/Crawler" -v /Users/lxs/workspace/Crawler:/root/Crawler -w=/root/Crawler -d --log-driver=fluentd --log-opt fluentd-address=114.212.189.147:10050 --log-opt tag=docker.{{.ID}} --log-opt fluentd-async-connect registry.njuics.cn/library/scrapy sh -c 'pip install -r requirements.txt && scrapy crawl spider'

docker run -e "SCRAPY_SETTINGS_MODULE=base.configs.wangyi_menhu.settings" -e "MONGO_HOST=114.212.189.140:31483" -e "MONGO_PORT=10094" -e "MONGO_DBNAME=Crawler" -e "PYTHONPATH=/root/Crawler" -d --log-driver=fluentd --log-opt fluentd-address=114.212.189.135:31426 --log-opt tag=docker.{{.ID}} --log-opt fluentd-async-connect scrapy-crawler:latest sh -c 'scrapy crawl spider'

java -cp target/mesos-crawler-1.0-SNAPSHOT-jar-with-dependencies.jar -Djava.library.path=/Users/lxs/Library/mesos/build/src/.libs cn.njuics.menya.mesos.TestFramework 127.0.0.1:5050

java -Djava.library.path=/Users/lxs/Library/mesos/build/src/.libs -jar -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005 target/cf-tutorial-mesos-docker-1.0-SNAPSHOT-jar-with-dependencies.jar 127.0.0.1:5050


docker run -d -p 24224:24224 -p 24224:24224/udp -v /Users/lxs/workspace/data:/fluentd/log fluent/fluentd:latest