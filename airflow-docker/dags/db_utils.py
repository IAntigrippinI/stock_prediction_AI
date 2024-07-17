import pandas as pd
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
        if symbol == "IBM" or symbol == "ibm":
            new_row = ibm()
        elif symbol == "MSFT" or symbol == "microsoft":
            new_row = microsoft()

        elif symbol == "AAPL" or symbol == "apple":
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


def get_table_for_metrics(name_db: str) -> pd.DataFrame:
    engine = create_engine(DB_URL)
    conn = engine.connect()
    data = conn.execute(f"SELECT date, close FROM {name_db}")
    df = pd.DataFrame(data, columns=["date", "close"])
    return df


def add_row_metric(row, symbol, metric):
    db_session = create_session()
    conn = db_session.connection()
    conn.execute(
        f"""INSERT INTO public.{symbol}_{metric} VALUES ('{str(row[0])}', {row[1]})"""
    )
    db_session.commit()
    db_session.close()


def add_row_macd(row, symbol):
    db_session = create_session()
    conn = db_session.connection()
    conn.execute(
        f"""INSERT INTO public.{symbol}_macd VALUES ('{str(row[0])}', {row[1]}, {row[2]})"""
    )
    db_session.commit()
    db_session.close()


def add_row_to_all(symbol, row):
    db_session = create_session()
    conn = db_session.connection()
    conn.execute(
        f"""
INSERT INTO all_data VALUES('{row[0]}', '{symbol}', {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}, {row[7]}, {row[8]})
"""
    )
    db_session.commit()
    db_session.close()
