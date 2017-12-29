FROM registry.njuics.cn/library/scrapy:latest

RUN echo "http://mirrors.aliyun.com/alpine/v3.7/main/" > /etc/apk/repositories

# Install ssh and git
RUN apk --update add openssh git mariadb-dev mariadb-client mariadb-libs

# Set pull access
ADD https://gist.githubusercontent.com/lxs137/57ebc9060bbe03c6706ec56abe789fd9/raw/41fe1324bd59b8de527b13976800772deffe8776/crawler.id_rsa /root/.ssh/id_rsa

RUN chmod 600 /root/.ssh/id_rsa \
	&& ssh-keyscan github.com >> /root/.ssh/known_hosts 

# Pull source code
RUN cd /root \
	&& git clone git@github.com:njunth/Crawler.git

RUN cd /root/Crawler \
	&& pip install -r requirements.txt

WORKDIR /root/Crawler

CMD ["sh", "scrapy crawl spider"]