from celery import Celery
from {{cookiecutter.project_slug}}.configs import settings

app = Celery('tasks', broker=settings.CELERY_BROKER_URL)


@app.task(name="{{cookiecutter.project_slug}}.pipeline.process_item")
def process_item(item):
    """
    Body method is defined here or something else (eg. in django project)
    """
    pass