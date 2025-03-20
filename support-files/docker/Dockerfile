FROM python:3.10
WORKDIR /apps

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/;
RUN rm -Rf /etc/apt/sources.list.d \
    && echo "deb http://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware" > /etc/apt/sources.list \
    && echo "deb http://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-backports main contrib non-free non-free-firmware" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list;

RUN apt-get update -y
RUN apt-get install -y vim supervisor

ADD ./support-files/supervisor/app.conf  /etc/supervisor/conf.d/app.conf
ADD ./support-files/supervisor/celery.conf  /etc/supervisor/conf.d/celery.conf
ADD ./support-files/supervisor/beat.conf  /etc/supervisor/conf.d/beat.conf
ADD ./support-files/supervisor/consumer.conf  /etc/supervisor/conf.d/consumer.conf
ADD ./support-files/supervisor/nats.conf  /etc/supervisor/conf.d/nats.conf

ADD . .

RUN pip install -r ./requirements/requirements-core.txt
RUN pip install -r ./requirements/requirements-dev.txt
RUN pip install -r ./requirements/requirements-ops.txt
RUN pip install -r ./requirements/requirements-extra.txt

RUN chmod +x ./support-files/docker/startup.sh
ENTRYPOINT ["/bin/bash","/apps/support-files/docker/startup.sh"]