import config

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine(config.db_url, pool_size=30)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
