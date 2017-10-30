# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CategoryItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    link = scrapy.Field()


class JokesItem(scrapy.Item):
    id = scrapy.Field()
    category_id = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    link = scrapy.Field()