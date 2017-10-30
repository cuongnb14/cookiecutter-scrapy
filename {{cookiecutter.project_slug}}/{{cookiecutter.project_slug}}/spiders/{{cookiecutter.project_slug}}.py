import scrapy
import sqlalchemy
from {{cookiecutter.project_slug}}.items import JokesItem
from {{cookiecutter.project_slug}}.models.base import session, CategoryModel


class {{cookiecutter.class_name}}Spider(scrapy.Spider):
    name = "{{cookiecutter.project_slug}}"
    BASE_URL = "http://www.google.com.vn"
    start_urls = [BASE_URL]

    def parse(self, response):
        pass
