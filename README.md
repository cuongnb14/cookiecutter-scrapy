# cookiecutter-scrapy

Powered by [Cookiecutter](https://github.com/audreyr/cookiecutter). Cookiecutter Scrapy is a framework for jumpstarting production-ready Scrapy projects quickly.

## Introduction
This cookie cutter is a very simple boilerplate for starting a scrapy project have support mysql pipeline. It comes with basic project structure and configuration.

**Features:**

- For Scrapy 1.5.1
- Simple scrapy project with MySQL pipiline
- Use docker for MySQL
- Use Makefile 

## Usage

Step 1: Init project

`cookiecutter https://github.com/cuongnb14/cookiecutter-scrapy.git`

Step 2: Install requirements

`make requirements`

Step 3: Run mysql container

`docker-compose up -d`

Step 4: Test crawl

`make crawl`