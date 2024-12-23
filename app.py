import os

from typing import Any
import psycopg2
from db_setup import get_connection
from fastapi import FastAPI, HTTPException, status, Depends
from db import create_user_db, get_user_db, update_user_db, delete_user_db, get_users_db,get_categories_db,get_exercise_db,get_exercises_db,get_record_db,get_repmax_db,get_workouts_db,update_exercise_db,update_records_db,update_repmax_db,update_workouts_db,create_category_db,create_exercise_db,create_record_db,create_repmax_db,create_workout_db,delete_category_db,delete_exercise_db,delete_record_db,delete_repmax_db
from schemas import UserCreate, UserUpdate
from psycopg2.errors import IntegrityError
app = FastAPI()

# Home


@app.get("/")
def get_status():
    """
    Confirms that we are up and running
    """
    return "Running on localhost:8000..."

#                                                        Users Endpoints


@app.get("/users/{user_id}", status_code=200)
def get_user(user_id: int):
    """
    Returns a user by ID

    Raises exception if user is not found
    """
    con = get_connection()
    user = get_user_db(con, user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/users", status_code=200)
def get_users():
    """
    Returns a list of all users
    """
    con = get_connection()
    return get_users_db(con)


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, con: Any = Depends(get_connection)):
    """
    Creates a user

    Raises exception if name already exists.
    Also raises exception if something went wrong when creating the user
    """
    try:
        result = create_user_db(con, user.password, user.name,
                                user.weight, user.user_record_id, user.weight)
        if result:
            return {'message': f'User created sucessfully with id: {result}'}
        raise HTTPException(
            detail='User not created properly', status_code=400)
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="Name already exists.")


@app.patch('/users/{user_id}', status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: UserUpdate, con: Any = Depends(get_connection)):
    """
    Updates one or more fields in a user by ID

    Raises exception if name already exists, or if no input was provided.

    """
    try:
        # Extract fields from UserUpdate and iterate over them
        # Only include fields that are set
        update_data = user.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No fields provided for update.")

        for column, value in update_data.items():
            # The function gets called for every row to enable the option to update serveral rows at once
            update_user_db(con, user_id, update_column=column,
                           update_value=value)

        return {'message': 'User updated successfully'}

    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="Username or email already exists.")


@app.delete('/users/{user_id}')
def delete_user(user_id: int, con: Any = Depends(get_connection)):
    """
    Deletes a user by ID

    Raises exception if user could not be found
    """
    result = delete_user_db(con, user_id)
    if result:
        return {'message': f'User with id {result['user_id']} deleted'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
