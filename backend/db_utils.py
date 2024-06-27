from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from cred import DB_URL
from models_sql import ibm


def create_session():
    engine = create_engine(DB_URL)
    SessionClass = sessionmaker(bind=engine)
    return SessionClass()


def get_last_date():
    db_session = create_session()
    last_date = db_session.query(ibm).order_by(desc(ibm.date)).first().date
    print(last_date)


if __name__ == "__main__":
    db_session = create_session()
    row = db_session.query(ibm).filter_by(open=123).first()
    print(row)
    row.high = 222
    db_session.commit()
