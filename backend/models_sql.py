from sqlalchemy import Column, Integer, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

import datetime

DeclBase = declarative_base()


class ibm(DeclBase):
    __tablename__ = "ibm"
    date = Column(DateTime, default=datetime.datetime.utcnow, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)


def create_table():
    from cred import DB_URL
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(DB_URL)
    SessionClass = sessionmaker(bind=engine)
    db_session = SessionClass()

    DeclBase.metadata.create_all(engine)
    db_session.commit()
