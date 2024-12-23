

import os

import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_NAME = os.getenv("DATABASE_NAME")
PASSWORD = os.getenv("PASSWORD")


def get_connection():
    """
    Function that returns a single connection
    In reality, we might use a connection pool, since
    this way we'll start a new connection each time
    someone hits one of our endpoints, which isn't great for performance
    """
    return psycopg2.connect(
        dbname=DATABASE_NAME,
        user="postgres",  # change if needed
        password=PASSWORD,
        host="localhost",  # change if needed
        port="5432",  # change if needed
    )


def create_tables():
    """
    A function to create the necessary tables for the project.
    """
    connection = get_connection()

    user_table = """ CREATE TABLE IF NOT EXISTS users(
        user_id SERIAL PRIMARY KEY,
        password VARCHAR(50),
        name VARCHAR(50) UNIQUE,
        weight BIGINT,
        user_record_id BIGINT,
        height BIGINT
    )
    """

    categories_table = """
    CREATE TABLE IF NOT EXISTS categories(
        category_id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE
    )
    """

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(categories_table)
            cursor.execute(user_table)


if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    create_tables()
    print("Tables created successfully.")
