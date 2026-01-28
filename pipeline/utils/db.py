import os
import psycopg2
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def get_conn():
    db_url = os.environ["DATABASE_URL"]
    return psycopg2.connect(db_url)
