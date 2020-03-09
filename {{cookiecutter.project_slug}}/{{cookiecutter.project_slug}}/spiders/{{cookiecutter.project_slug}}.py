import scrapy
import sqlalchemy
from {{cookiecutter.project_slug}}.items import JokesItem


class {{cookiecutter.class_name}}Spider(scrapy.Spider):
    name = "{{cookiecutter.project_slug}}"
    BASE_URL = "http://www.google.com.vn"
    start_urls = [BASE_URL]

    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         '{{cookiecutter.project_slug}}.pipelines.celery.CeleryPipeline': 100,
    #     },
    # }

    def parse(self, response):
        self.logger.info(str(response))
