
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from data.constants import CONNECTION_ROW


Model = declarative_base(name='Model')
engine = create_engine(CONNECTION_ROW)
Session = sessionmaker(engine, autoflush=False)


def add_to_db(get_db_session, data):
    get_db_session.add(data)
    get_db_session.commit()




