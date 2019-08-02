import os
import psycopg2
from env_loader import load_env_config


def create_db():
    load_env_config()

    # Will connect to the user database
    print("Connecting to default database...")
    connection = psycopg2.connect(os.getenv("DEFAULT_SQL_DATABASE_URI"))
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = '"+os.getenv("SQL_DATABASE_NAME")+"'")
    exists = cursor.fetchone()

    if not exists:
        print("Creating application database...")
        cursor.execute('CREATE DATABASE '+os.getenv("SQL_DATABASE_NAME")+' OWNER '+os.getenv("SQL_DATABASE_USER"))
        cursor.execute('GRANT ALL PRIVILEGES ON DATABASE '+os.getenv("SQL_DATABASE_NAME")+' TO '+os.getenv("SQL_DATABASE_USER"))
        cursor.close()
        connection.close()

        print("Connecting to application database...")
        connection = psycopg2.connect(os.getenv("SQLALCHEMY_DATABASE_URI"))
        connection.autocommit = True
        cursor = connection.cursor()

        print("Creating extensions...")
        cursor.execute("""CREATE EXTENSION IF NOT EXISTS "uuid-ossp";""")

    cursor.close()
    connection.close()
    print("Closed connections")


if __name__ == "__main__":
    create_db()