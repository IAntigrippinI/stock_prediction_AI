from sqlalchemy import Column, Integer, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

import datetime 
DeclBase = declarative_base()

class IBM(DeclBase):
    __tablename__ = 'IBM'
    id = Column(Integer,primary_key=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)


if __name__ == '__main__':
    from backend.cred import DB_URL
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(DB_URL)
    SessionClass = sessionmaker(bind=engine)
    db_session = SessionClass()

    DeclBase.metadata.create_all(engine)
    db_session.commit()