FROM python:3.10
WORKDIR /apps

RUN apt-get update -y
RUN apt-get install -y vim supervisor

ADD ./support-files/supervisor/app.conf  /etc/supervisor/conf.d/app.conf
ADD ./support-files/supervisor/celery.conf  /etc/supervisor/conf.d/celery.conf
ADD ./support-files/supervisor/beat.conf  /etc/supervisor/conf.d/beat.conf

ADD . .

RUN pip install -r ./requirements/requirements-core.txt
RUN pip install -r ./requirements/requirements-dev.txt
RUN pip install -r ./requirements/requirements-ops.txt
RUN pip install -r ./requirements/requirements-extra.txt

RUN chmod +x ./support-files/docker/startup.sh
ENTRYPOINT ["/bin/bash","/apps/support-files/docker/startup.sh"]