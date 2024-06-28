from sqlalchemy import create_engine
import pandas as pd


engine = create_engine('postgresql://polina:polina@localhost/postgres')
df = pd.read_sql_table('ibm', engine)

df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

df = df.resample('D').agg({'open': 'first', 
                           'high': 'max', 
                           'low': 'min', 
                           'close': 'last'}).dropna()