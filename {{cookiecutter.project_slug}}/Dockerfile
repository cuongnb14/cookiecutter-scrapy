FROM ubuntu:18.04
LABEL maintainer="{{cookiecutter.email}}"

ENV REFRESHED_AT 2018-12-28

RUN apt-get update -qq

RUN apt-get install -y locales && locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip \
    libxml2-dev libxslt1-dev libssl-dev libffi-dev

WORKDIR /build

COPY requirements.txt /build/requirements.txt
RUN pip3 install -r requirements.txt

COPY . /build

RUN chmod +x start.sh

CMD ["./start.sh"]