from {{cookiecutter.project_slug}}.celery.app import process_item


class DemoPipeline(object):

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        process_item.delay(dict(item))
        return item