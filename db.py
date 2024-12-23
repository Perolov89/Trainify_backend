import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException, status
from psycopg2.errors import ForeignKeyViolation

# This file is responsible for making database queries,
# which the fastapi endpoints/routes can use.

#                                                       Users
def get_user_db(con, user_id: int):
    """
    Fetches one user based on the id
    raises: Error if movie was not found
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                           SELECT * FROM users
                           WHERE user_id = %s
                           """,
                (user_id,),
            )
            result = cursor.fetchone()
            if result:
                return result
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


def get_users_db(con):
    """
    Fetches all users
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                           SELECT * FROM users;
                           """
            )
            result = cursor.fetchall()
            return result


def create_user_db(con, password,name,weight,user_record_id,height):
    """
    Creates new user

    Raises exception if invalid user_id is provided
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    INSERT INTO users(password,name,weight,user_record_id,height)
                    VALUES(%s,%s,%s,%s,%s)
                    RETURNING user_id
                    """,
                    (name, password, name, weight, user_record_id, height),
                )
                result = cursor.fetchone()
                if result:
                    print(f"User {name} was created successfully!")
                    return result['user_id']
    except ForeignKeyViolation:
        # Transaction will automatically rollback due to the context manager
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id or realtor_id provided"
        )


def update_user_db(con, user_id: int, update_column: str, update_value: str):
    """
    Update one or more values in user

    Raises exception if no value is passed or the column name is invalid
    Also raises exception if the user is not found 
    """

    # Validation to avoid sql-injection
    valid_columns = {'name', 'password', 'name', 'weight', 'user_record_id', 'height'}
    if update_column not in valid_columns:
        raise ValueError(f"Invalid column name: {update_column}")

    # Check if value is empty
    if not update_value:
        raise ValueError('No value was passed')

    query = f"""
            UPDATE users
            SET {update_column} = %s
            WHERE user_id = %s
            RETURNING user_id;
            """

    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (update_value, user_id))
            result = cursor.fetchone()
            if result:
                print(f"User was updated successfully!")
                return result
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


def delete_user_db(con, user_id: int):
    """
    Delete a user by ID

    Raises exception if user is not found
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                           DELETE FROM users
                           WHERE user_id = %s
                           RETURNING user_id;
                           """,
                (user_id,),
            )
            result = cursor.fetchone()
            if result:
                print(f"User was deleted successfully!")
                return result
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)



#                                                   Exercises

def get_exercises_db(con):
    """
    Fetches all users
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                           SELECT * FROM exercises;
                           """
            )
            result = cursor.fetchall()
            return result

def get_exercise_db(con, exercise_id: int):
    """
    Fetches one exercise based on the id
    raises: Error if movie was not found
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                           SELECT * FROM exercises
                           WHERE exercise_id = %s
                           """,
                (exercise_id,),
            )
            result = cursor.fetchone()
            if result:
                return result
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


def create_exercise_db(con, exercise_name,exercise_weight,repmax_id,primary_muscle_id,secondary_muscle_id,category_id):
    """
    Creates new exercise

    Raises exception if invalid repmax_id, primary_muscle_id,secondary_muscle_id or categpory_id is provided
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    INSERT INTO exercises(exercise_name,exercise_weight,repmax_id,primary_muscle_id,secondary_muscle_id,category_id)
                    VALUES(%s,%s,%s,%s,%s,%s)
                    RETURNING exercise_id
                    """,
                    (exercise_name,exercise_weight,repmax_id,primary_muscle_id,secondary_muscle_id,category_id),
                )
                result = cursor.fetchone()
                if result:
                    print(f"Exercise {exercise_name} was created successfully!")
                    return result['exercise_id']
    except ForeignKeyViolation:
        # Transaction will automatically rollback due to the context manager
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid repmax_id, primary_muscle_id,secondary_muscle_id or categpory_id provided"
        )


def update_exercise_db(con, exercise_id: int, update_column: str, update_value: str):
    """
    Update one or more values in exercises

    Raises exception if no value is passed or the column name is invalid
    Also raises exception if the exercise is not found 
    """

    # Validation to avoid sql-injection
    valid_columns = {'exercise_name', 'exercise_weight', 'repmax_id', 'primary_muscle_id', 'secondary_muscle_id', 'category_id'}
    if update_column not in valid_columns:
        raise ValueError(f"Invalid column name: {update_column}")

    # Check if value is empty
    if not update_value:
        raise ValueError('No value was passed')

    query = f"""
            UPDATE exercises
            SET {update_column} = %s
            WHERE exercise_id = %s
            RETURNING exercise_id;
            """

    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (update_value, exercise_id))
            result = cursor.fetchone()
            if result:
                print(f"Exercise was updated successfully!")
                return result
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


def delete_exercise_db(con, exercise_id: int):
    """
    Delete a exercise by ID

    Raises exception if exercise is not found
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                           DELETE FROM exercise
                           WHERE exercise_id = %s
                           RETURNING exercise_id;
                           """,
                (exercise_id,),
            )
            result = cursor.fetchone()
            if result:
                print(f"Exercise was deleted successfully!")
                return result
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        

#                                                    Records
        

def get_record_db(con):
    """
    Fetches all records
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                           SELECT * FROM records;
                           """
            )
            result = cursor.fetchall()
            return result


def create_record_db(con, workout_id, user_id,record_time):
    """
    Creates new record

    Raises exception if invalid user_id is provided
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    INSERT INTO records(workout_id, user_id, record_time)
                    VALUES(%s,%s,%s)
                    RETURNING user_id
                    """,
                    (workout_id,user_id,record_time),
                )
                result = cursor.fetchone()
                if result:
                    print(f"Record for workout with id:{workout_id} was created successfully!")
                    return result['user_id']
    except ForeignKeyViolation:
        # Transaction will automatically rollback due to the context manager
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id or workout_id provided"
        )


def update_records_db(con, record_id: int, update_column: str, update_value: str):
    """
    Update one or more values in records

    Raises exception if no value is passed or the column name is invalid
    Also raises exception if the record is not found 
    """

    # Validation to avoid sql-injection
    valid_columns = {'workout_id', 'user_id', 'record_time'}
    if update_column not in valid_columns:
        raise ValueError(f"Invalid column name: {update_column}")

    # Check if value is empty
    if not update_value:
        raise ValueError('No value was passed')

    query = f"""
            UPDATE records
            SET {update_column} = %s
            WHERE record_id = %s
            RETURNING record_id;
            """

    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (update_value, record_id))
            result = cursor.fetchone()
            if result:
                print(f"Record was updated successfully!")
                return result
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


def delete_record_db(con, record_id: int):
    """
    Delete a record by ID

    Raises exception if record is not found
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                           DELETE FROM records
                           WHERE record_id = %s
                           RETURNING record_id;
                           """,
                (record_id,),
            )
            result = cursor.fetchone()
            if result:
                print(f"Record was deleted successfully!")
                return result
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
