import os
import psycopg2

def get_conn():
    db_url = os.environ["DATABASE_URL"]
    return psycopg2.connect(db_url)
