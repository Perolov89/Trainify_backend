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
        user="postgres",  # Update if needed
        password=PASSWORD,
        host="localhost",  # Update if needed
        port="5432",  # Update if needed
    )


def insert_data():
    """
    Inserts data into the tables.
    """
    connection = get_connection()

    inserts = [
        # Roles
        "INSERT INTO roles (name) VALUES ('Admin'), ('Realtor'), ('Buyer')",

        # Users
        """
        INSERT INTO users (username, email, password, role_id, realtor_id) VALUES
        ('admin', 'admin@example.com', 'securepassword1', 1, NULL),
        ('realtor_john', 'john@example.com', 'securepassword2', 2, 1),
        ('buyer_emily', 'emily@example.com', 'securepassword3', 3, NULL)
        """,

        # Address

    ]

    with connection:
        with connection.cursor() as cursor:
            for sql in inserts:
                cursor.execute(sql)

    print("Data inserted successfully.")


if __name__ == "__main__":
    insert_data()