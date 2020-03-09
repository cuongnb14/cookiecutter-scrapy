import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base

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