from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.cred import DB_URL


def create_session():
    engine = create_engine(DB_URL)
    SessionClass = sessionmaker(bind=engine)
    return SessionClass()
