from {{cookiecutter.project_slug}}.configs.settings import DB
from {{cookiecutter.project_slug}}.models.models import Base
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


def get_session():
    engine_url = sqlalchemy.engine.url.URL(
        drivername=DB["dialect"],
        host=DB["host"],
        port=DB["port"],
        username=DB["username"],
        password=DB["password"],
        database=DB["db_name"],
        # query={'charset': 'utf8mb4'}
    )

    db_engine = create_engine(engine_url, encoding='utf-8', echo=False, pool_recycle=3600)

    Session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = scoped_session(Session)
    return db_engine, session


_, session = get_session()

# def create_backup_schema():
#     """
#     Create schema
#
#     """
#     Base.metadata.create_all(db_engine)
