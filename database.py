from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
import os
import psycopg2
load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL'].replace("postgres://", "postgresql://", 1)
"""usr = os.getenv("db_usr")
pwd = os.getenv("db_pwd")
hostname = os.getenv("db_hostname")
db_name = os.getenv("db_name")
db_driver = os.getenv("db_driver")  # postgresql+psycopg2
db_uri = os.getenv("db_uri")

DATABASE_URL = f'{db_driver}://{usr}:{pwd}@{hostname}/{db_name}'"""


sqlEngine = create_engine(DATABASE_URL)

conn = sqlEngine.connect()


def manage_db_watch_data(watch_data: dict):
    forbidden = ['preferences', 'stress_histogram']
    for key in watch_data.keys():
        if key.replace('.', '_') not in forbidden:
            watch_data[key].to_sql(key.replace('.', '_'), con=conn, if_exists='replace', index=False)

    stages_data_mapping = {'id': [4001, 4002, 4003, 4004], "stages": ['LIGHT', 'DEEP', 'REM', 'AWAKE']}
    sleep_stages = pd.DataFrame(stages_data_mapping)
    sleep_stages.to_sql('sleep_stages_mapping', con=conn, if_exists='replace', index=False)


def manage_db_renpho_data(renpho_data: dict):
    try:
        scale_data_stored = pd.read_sql('scale_data', conn)

        result = scale_data_stored.append(renpho_data['scale'])
        result.drop_duplicates(keep='last', inplace=True)
        result.to_sql('scale_data', con=conn, if_exists='append', index=False)
    except:
        renpho_data['scale'].to_sql('scale_data', con=conn, if_exists='append', index=False)


def get_connection():
    return conn
