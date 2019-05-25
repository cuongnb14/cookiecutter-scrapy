all: crawl

build:
	docker build -t {{cookiecutter.project_slug}}:{{cookiecutter.version}} .
	
crawl:
	scrapy crawl {{cookiecutter.project_slug}}

requirements:
	pip install -r requirements.txt