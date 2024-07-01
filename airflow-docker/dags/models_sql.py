from sqlalchemy import Column, Float, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

import datetime

DeclBase = declarative_base()


class ibm(DeclBase):
    __tablename__ = "ibm"
    date = Column(TIMESTAMP, default=datetime.datetime.utcnow(), primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)


class microsoft(DeclBase):
    __tablename__ = "microsoft"
    date = Column(TIMESTAMP, default=datetime.datetime.utcnow(), primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)


class apple(DeclBase):
    __tablename__ = "apple"
    date = Column(TIMESTAMP, default=datetime.datetime.utcnow(), primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)


class apple_predict(DeclBase):
    __tablename__ = "apple_predict"
    date = Column(TIMESTAMP, default=datetime.datetime.utcnow(), primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)


class ibm_predict(DeclBase):
    __tablename__ = "ibm_predict"
    date = Column(TIMESTAMP, default=datetime.datetime.utcnow(), primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)


class microsoft_predict(DeclBase):
    __tablename__ = "microsoft_predict"
    date = Column(TIMESTAMP, default=datetime.datetime.utcnow(), primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)


def create_table():
    from cred_airflow import DB_URL
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(DB_URL)
    SessionClass = sessionmaker(bind=engine)
    db_session = SessionClass()

    DeclBase.metadata.create_all(engine)
    db_session.commit()
