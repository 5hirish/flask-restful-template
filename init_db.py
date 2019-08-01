import os
import psycopg2
from dotenv import load_dotenv


def create_db():
    load_dotenv()

    connection = psycopg2.connect(os.getenv("DATABASE_URL"))
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = '"+os.getenv("DATABASE_NAME")+"'")
    exists = cursor.fetchone()

    if not exists:
        cursor.execute('CREATE DATABASE '+os.getenv("DATABASE_NAME"))

    cursor.close()
    connection.close()


if __name__ == "__main__":
    create_db()