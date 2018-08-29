import datetime

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from {{cookiecutter.project_slug}}.settings import MYSQL

Base = declarative_base()


class TimeStampedModelMixin:
    """
     An Mixin base class model that provides self-updating
    ``created_at`` and ``modified_at`` fields.
    """
    created_at = Column(DateTime, default=datetime.datetime.now)
    modified_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class CategoryModel(TimeStampedModelMixin, Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(String(255))
    link = Column(String(1000))


class JokesModel(TimeStampedModelMixin, Base):
    __tablename__ = 'jokes'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    content = Column(Text())
    category_id = Column(Integer, ForeignKey("category.id"))
    link = Column(String(1000))





engine_url = sqlalchemy.engine.url.URL(
                drivername=MYSQL["dialect"],
                host=MYSQL["host"],
                port=MYSQL["port"],
                username=MYSQL["username"],
                password=MYSQL["password"],
                database=MYSQL["db_name"],
                query={'charset': 'utf8'}
        )

db_engine = create_engine(engine_url, encoding='utf-8', echo=False, pool_recycle=3600)
Session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
session = scoped_session(Session)


def create_schema():
    """
    Drop schema if exists and create schema

    """
    Base.metadata.drop_all(db_engine)
    Base.metadata.create_all(db_engine)
