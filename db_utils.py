import psycopg
import os
from dotenv import load_dotenv

load_dotenv()


def get_db_connection(db_name):
    return psycopg.connect(
        dbname=db_name,
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
