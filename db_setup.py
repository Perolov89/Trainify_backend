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
        user="postgres",
        password=PASSWORD,
        host="localhost",
        port="5432",
    )


def create_tables():
    """
    A function to create the necessary tables for the project.
    """
    connection = get_connection()

    # Define the SQL statements to create the tables
    user_table = """ 
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        password VARCHAR(100) NOT NULL,
        name VARCHAR(250) UNIQUE NOT NULL,
        weight BIGINT NOT NULL,
        user_record_id BIGINT,
        height BIGINT
    );
    """

    categories_table = """
    CREATE TABLE IF NOT EXISTS categories (
        category_id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL
    );
    """

    exercises_table = """
    CREATE TABLE IF NOT EXISTS exercises (
        exercise_id SERIAL PRIMARY KEY,
        exercise_name VARCHAR(250) NOT NULL,
        exercise_weight BIGINT NOT NULL,
        repmax_id BIGINT,
        primary_muscle VARCHAR(100),
        secondary_muscle VARCHAR(100),
        category_id INT NOT NULL,
        base_exercise BOOL NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories (category_id) ON DELETE CASCADE
    );
    """

    records_table = """
    CREATE TABLE IF NOT EXISTS records (
        record_id SERIAL PRIMARY KEY,
        workout_id BIGINT NOT NULL,
        user_id INT NOT NULL,
        record_time TIMESTAMP NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
    );
    """

    repmax_table = """
    CREATE TABLE IF NOT EXISTS repmax (
        repmax_id SERIAL PRIMARY KEY,
        exercise_id INT NOT NULL,
        user_id INT NOT NULL,
        weight BIGINT NOT NULL,
        FOREIGN KEY (exercise_id) REFERENCES exercises (exercise_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
    );
    """

    workouts_table = """
    CREATE TABLE IF NOT EXISTS workouts (
        workout_id SERIAL PRIMARY KEY,
        workout_name VARCHAR(250) NOT NULL,
        timecap BIGINT NOT NULL,
        record_id INT NOT NULL,
        exercise_id INT NOT NULL,
        for_kids BOOL,
        FOREIGN KEY (record_id) REFERENCES records (record_id) ON DELETE CASCADE,
        FOREIGN KEY (exercise_id) REFERENCES exercises (exercise_id) ON DELETE CASCADE
    );
    """,

    workout_exercises_table = """
    CREATE TABLE workout_exercises (
    workout_exercise_id SERIAL PRIMARY KEY,
    workout_id INT NOT NULL,
    exercise_id INT NOT NULL,
    sets INT DEFAULT 0,
    reps INT DEFAULT 0,
    rest_time BIGINT DEFAULT 0,
    FOREIGN KEY (workout_id) REFERENCES workouts (workout_id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises (exercise_id) ON DELETE CASCADE
    );
    """


    # Execute the table creation statements
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(user_table)
            cursor.execute(categories_table)
            cursor.execute(exercises_table)
            cursor.execute(records_table)
            cursor.execute(repmax_table)
            cursor.execute(workouts_table)
            cursor.execute(workout_exercises_table)

if __name__ == "__main__":
    # Execute the script to create tables
    create_tables()
    print("Tables created successfully.")
