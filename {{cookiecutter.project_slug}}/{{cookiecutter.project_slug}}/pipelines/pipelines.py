# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from {{cookiecutter.project_slug}}.models.models import JokesModel
from {{cookiecutter.project_slug}}.models.sessions import session
from sqlalchemy import exists


class MySQLPipeline(object):
    """Pipeline to save jokes to mysql database"""

    def close_spider(self, spider):
        session.close()

    def process_item(self, item, spider):
        jokes = self.__get_jokes(item)
        if jokes:
            session.add(jokes)
            session.commit()
        return item

    def __get_jokes(self, item):
        jokes = session.query(exists().where(JokesModel.link == item.get("link"))).scalar()
        if jokes:
            return None

        jokes = JokesModel()
        jokes.title = item.get("title")
        jokes.category_id = item.get("category_id")
        jokes.link = item.get("link")
        jokes.content = item.get("content")
        return jokes
