import config

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine(
    config.db_url
)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
