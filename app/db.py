from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base
from .test_db_data import test_data
from os import environ

DB_NAME = environ.get('DB_NAME', 'localhost')

engine = create_engine(f'postgresql+pg8000://postgres:@{DB_NAME}/pharmacy')

session_factory = scoped_session(sessionmaker(
    autoflush=True,
    bind=engine
))

def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with session_factory() as session:
        session.add_all(test_data)
        session.commit()
    print("Database was reinitialized")