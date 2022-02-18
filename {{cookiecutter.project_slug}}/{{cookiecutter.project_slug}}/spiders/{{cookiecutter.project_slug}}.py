import scrapy
import sqlalchemy
from {{cookiecutter.project_slug}}.items import JokesItem


class {{cookiecutter.class_name}}Spider(scrapy.Spider):
    name = "{{cookiecutter.project_slug}}"
    BASE_URL = "http://www.google.com.vn"

    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         '{{cookiecutter.project_slug}}.pipelines.celery.CeleryPipeline': 100,
    #     },
    # }

    def start_requests(self):
        yield scrapy.Request(BASE_URL, callback=self.parse)

    def parse(self, response, *args, **kwargs):
        self.logger.info(str(response))
