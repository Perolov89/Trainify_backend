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
    raises: Error if user was not found
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


def create_user_db(con, password, name, weight, user_record_id, height):
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
    valid_columns = {'name', 'password', 'name',
                     'weight', 'user_record_id', 'height'}
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


def create_exercise_db(con, exercise_name, exercise_weight, repmax_id, primary_muscle, secondary_muscle, category_id, base_exercise):
    """
    Creates new exercise

    Raises exception if invalid repmax_id or categpory_id is provided
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    INSERT INTO exercises(exercise_name,exercise_weight,repmax_id,primary_muscle,secondary_muscle,category_id, base_exercise)
                    VALUES(%s,%s,%s,%s,%s,%s,%s)
                    RETURNING exercise_id
                    """,
                    (exercise_name, exercise_weight, repmax_id,
                     primary_muscle, secondary_muscle, category_id, base_exercise),
                )
                result = cursor.fetchone()
                if result:
                    print(f"Exercise {
                          exercise_name} was created successfully!")
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
    valid_columns = {'exercise_name', 'exercise_weight', 'repmax_id',
                     'primary_muscle', 'secondary_muscle', 'category_id', 'base_exercise'}
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


def get_record_db(con, user_id: int):
    """
    Fetches one record based on the id
    raises: Error if user was not found
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                           SELECT * FROM records
                           WHERE user_id = %s
                           """,
                (user_id,),
            )
            result = cursor.fetchone()
            if result:
                return result
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


def get_records_db(con):
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


def create_record_db(con, workout_id, user_id, record_time):
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
                    RETURNING record_id
                    """,
                    (workout_id, user_id, record_time),
                )
                result = cursor.fetchone()
                if result:
                    print(f"Record for workout with id:{
                          workout_id} was created successfully!")
                    return result['record_id']
    except ForeignKeyViolation:
        # Transaction will automatically rollback due to the context manager
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id or workout_id provided"
        )


def update_records_db(con, record_id: int, record_time: str):
    """
    Update one or more values in records

    Raises exception if no value is passed
    Also raises exception if the record is not found 
    """
    # Check if value is empty

    if not record_time:
        raise ValueError('No value was passed')
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                            UPDATE records
                            SET record_time = %s
                            WHERE record_id = %s
                            RETURNING record_id;
                            """, (record_time, record_id))
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


#                                               Repmaxes


def get_repmax_db(con):
    """
    Fetches all repmax's
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                           SELECT * FROM repmax;
                           """
            )
            result = cursor.fetchall()
            return result


def create_repmax_db(con, exercise_id, user_id, weight):
    """
    Creates new repmax

    Raises exception if invalid user_id is provided
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    INSERT INTO repmax(exercise_id, user_id, weight)
                    VALUES(%s,%s,%s)
                    RETURNING repmax_id
                    """,
                    (exercise_id, user_id, weight),
                )
                result = cursor.fetchone()
                if result:
                    print(f"Repmax for exercise with id:{
                          exercise_id} was created successfully!")
                    return result['repmax_id']
    except ForeignKeyViolation:
        # Transaction will automatically rollback due to the context manager
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id or workout_id provided"
        )


def update_repmax_db(con, repmax_id: int, update_column: str, update_value: str):
    """
    Update one or more values in repmax

    Raises exception if no value is passed or the column name is invalid
    Also raises exception if the record is not found 
    """

    # Validation to avoid sql-injection
    valid_columns = {'weight'}
    if update_column not in valid_columns:
        raise ValueError(f"Invalid column name: {update_column}")

    # Check if value is empty
    if not update_value:
        raise ValueError('No value was passed')

    query = f"""
            UPDATE repmax
            SET {update_column} = %s
            WHERE weight = %s
            RETURNING repmax_id;
            """

    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (update_value, repmax_id))
            result = cursor.fetchone()
            if result:
                print(f"Weight for repmax was updated successfully!")
                return result
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


def delete_repmax_db(con, repmax_id: int):
    """
    Delete a repmax by ID

    Raises exception if repmax is not found
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                           DELETE FROM repmax
                           WHERE repmax_id = %s
                           RETURNING repmax_id;
                           """,
                (repmax_id,),
            )
            result = cursor.fetchone()
            if result:
                print(f"Repmax was deleted successfully!")
                return result
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


#                                               workouts


def get_workouts_db(con):
    """
    Fetches all workouts
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                           SELECT * FROM workouts;
                           """
            )
            result = cursor.fetchall()
            return result


def create_workout_db(con, workout_name, timecap, record_id, exercise_id):
    """
    Creates new workout

    Raises exception if invalid user_id is provided
    """
    try:
        with con:
            with con.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    INSERT INTO workouts(workout_name,timecap,record_id,exercise_id)
                    VALUES(%s,%s,%s,%s)
                    RETURNING workout_id
                    """,
                    (workout_name, timecap, record_id, exercise_id),
                )
                result = cursor.fetchone()
                if result:
                    print(f"Workout {workout_name} was created successfully!")
                    return result['workout_id']
    except ForeignKeyViolation:
        # Transaction will automatically rollback due to the context manager
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id or exercise_id provided"
        )


def update_workouts_db(con, workout_id: int, update_column: str, update_value: str):
    """
    Update one or more values in workouts

    Raises exception if no value is passed or the column name is invalid
    Also raises exception if the record is not found 
    """

    # Validation to avoid sql-injection
    valid_columns = {'workout_name', 'timecap', 'record_id', 'exercise_id'}
    if update_column not in valid_columns:
        raise ValueError(f"Invalid column name: {update_column}")

    # Check if value is empty
    if not update_value:
        raise ValueError('No value was passed')

    query = f"""
            UPDATE workouts
            SET {update_column} = %s
            WHERE workout_id = %s
            RETURNING workout_id;
            """

    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (update_value, workout_id))
            result = cursor.fetchone()
            if result:
                print(f"Workout was updated successfully!")
                return result
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


def delete_record_db(con, workout_id: int):
    """
    Delete a workout by ID

    Raises exception if workout is not found
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                           DELETE FROM workouts
                           WHERE workout_id = %s
                           RETURNING workout_id;
                           """,
                (workout_id,),
            )
            result = cursor.fetchone()
            if result:
                print(f"Workout was deleted successfully!")
                return result
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


#                                                   Categories

def get_categories_db(con):
    """
    Fetches all categories
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                           SELECT * FROM categories;
                           """
            )
            result = cursor.fetchall()
            return result


def create_category_db(con, category_name):
    """
    Creates new category

    """

    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO categories(category_name)
                VALUES(%s)
                RETURNING category_id
                """,
                (category_name),
            )
            result = cursor.fetchone()
            if result:
                print(f"Category {category_name} was created successfully!")
                return result['category_id']
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


def delete_category_db(con, category_id: int):
    """
    Delete a category by ID

    Raises exception if category is not found
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                           DELETE FROM categories
                           WHERE cateogry_id = %s
                           RETURNING category_id;
                           """,
                (category_id,),
            )
            result = cursor.fetchone()
            if result:
                print(f"Category was deleted successfully!")
                return result
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
