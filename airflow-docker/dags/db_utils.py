from datetime import datetime
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from cred_airflow import DB_URL
from models_sql import (
    ibm,
    apple,
    microsoft,
    apple_predict,
    ibm_predict,
    microsoft_predict,
)


def create_session():
    engine = create_engine(DB_URL)
    SessionClass = sessionmaker(bind=engine)
    return SessionClass()


def create_cursor():
    conn = create_engine(DB_URL).connect()
    return conn


def delete_from_table(name_table):
    try:
        last_row = list(
            create_engine(DB_URL).connect().execute(f"DELETE FROM {name_table}")
        )
        return "succes delete"
    except:
        return "Error"


def get_last_date(symbol):

    db_session = create_session()
    if symbol == "ibm":
        last_date = db_session.query(ibm).order_by(desc(ibm.date)).first().date
    elif symbol == "apple":
        last_date = db_session.query(apple).order_by(desc(apple.date)).first().date
    else:
        last_date = (
            db_session.query(microsoft).order_by(desc(microsoft.date)).first().date
        )
    return last_date


def is_record(symbol: str) -> bool:

    count = list(
        create_cursor().execute(f"SELECT count(date) FROM public.{symbol} limit 1")
    )[0][0]

    print(count)
    if count == 0:
        return False
    else:
        return True


def add_row(row: list, symbol: str):
    try:
        db_session = create_session()
        if symbol == "IBM":
            new_row = ibm()
        elif symbol == "MSFT":
            new_row = microsoft()

        elif symbol == "AAPL":
            new_row = apple()

        new_row.date = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        new_row.open = row[1]
        new_row.high = row[2]
        new_row.low = row[3]
        new_row.close = row[4]
        new_row.volume = row[5]
        db_session.add(new_row)
        db_session.commit()

    except Exception as e:
        print(f"Error with add row {symbol} : {e}")


def add_row_predict(row: list, symbol: str):
    try:
        db_session = create_session()
        if symbol == "ibm":
            new_row = ibm_predict()

        elif symbol == "microsoft":
            new_row = microsoft_predict()

        elif symbol == "apple":
            new_row = apple_predict()

        new_row.date = row[0]
        new_row.open = row[1]
        new_row.high = row[2]
        new_row.low = row[3]
        new_row.close = row[4]
        db_session.add(new_row)
        db_session.commit()
    except Exception as e:
        print(f"Error with add row {symbol} : {e}")


def get_last_date(symbol) -> str:
    last_date = list(
        create_cursor().execute(
            f"SELECT date FROM public.{symbol} order by date DESC limit 1"
        )
    )[0][0]

    return str(last_date)


if __name__ == "__main__":
    db_session = create_session()
    row = db_session.query(ibm).filter_by(open=123).first()
    print(row)
    row.high = 222
    db_session.commit()
