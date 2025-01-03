import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_NAME = os.getenv("DATABASE_NAME")
PASSWORD = os.getenv("PASSWORD")


def get_connection():
    """
    Establishes a database connection.
    """
    return psycopg2.connect(
        dbname=DATABASE_NAME,
        user="postgres",
        password=PASSWORD,
        host="localhost",
        port="5432",
    )


def insert_data():
    """
    Inserts data into the tables.
    """
    connection = get_connection()

    inserts = [
        # Users
        """
        INSERT INTO users (password, name, weight, user_record_id, height) VALUES
        ('password123', 'john_doe', 75, NULL, 180),
        ('securePass456', 'jane_smith', 68, NULL, 165),
        ('gymLover789', 'mike_tyson', 95, NULL, 178);

        """,

        # Categories
        """INSERT INTO categories (name) VALUES
        ('Strength'),
        ('Cardio'),
        ('Flexibility'),
        ('Endurance');
        """,

        # Exercises

        """
        INSERT INTO exercises (exercise_name, exercise_weight, repmax_id, primary_muscle, secondary_muscle, category_id) VALUES
        ('Bench Press', 80, NULL, 'Chest', 'Triceps', 1),
        ('Squats', 100, NULL, 'Legs', 'Glutes', 1),
        ('Deadlift', 120, NULL, 'Back', 'Legs', 1),
        ('Running', 0, NULL, 'Legs', NULL, 2),
        ('Yoga Stretch', 0, NULL, 'Full Body', NULL, 3);
        """,

        # Records
        """
        INSERT INTO records (workout_id, user_id, record_time) VALUES
        (1, 1, '2025-01-01 10:00:00'),
        (2, 2, '2025-01-02 11:00:00'),
        (3, 3, '2025-01-03 12:00:00');
        """,
        # Repmax
        """INSERT INTO repmax (exercise_id, user_id, weight) VALUES
        (1, 1, 80),
        (2, 2, 100),
        (3, 3, 120);
        """,

        # Workouts
        """INSERT INTO workouts (workout_name, timecap, record_id, exercise_id, for_kids) VALUES
        ('Full Body Workout', 30, 1, 1, FALSE),
        ('Leg Day', 45, 2, 2, FALSE),
        ('Back and Core', 50, 3, 3, TRUE);
        """,
    ]

    with connection:
        with connection.cursor() as cursor:
            for sql in inserts:
                cursor.execute(sql)

    print("Data inserted successfully.")


if __name__ == "__main__":
    insert_data()
