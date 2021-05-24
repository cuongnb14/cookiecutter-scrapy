FROM ubuntu:20.04

RUN apt-get update -qq

RUN apt-get install -y locales && locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip \
    libxml2-dev libxslt1-dev libssl-dev libffi-dev cron curl

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY crontab/schedule /etc/cron.d/schedule
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/schedule
# Apply cron job
RUN crontab /etc/cron.d/schedule

COPY . /app

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]