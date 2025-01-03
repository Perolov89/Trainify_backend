import os

from typing import Any, List
import psycopg2
from db_setup import get_connection
from fastapi import FastAPI, HTTPException, status, Depends
from db import create_user_db, get_user_db, update_user_db, delete_user_db, get_users_db, get_records_db, get_categories_db, get_exercise_db, get_exercises_db, get_record_db, get_workout_db, get_repmaxs_db, get_workouts_db, update_records_db, update_repmax_db, update_workout_db, create_category_db, create_exercise_db, create_record_db, create_repmax_db, create_workout_db, delete_category_db, delete_exercise_db, delete_record_db, delete_repmax_db, delete_workout_db, get_workout_exercises_by_workout_id_db, get_workout_exercises_db, create_workout_exercise_db, delete_workout_exercise_db, update_workout_exercise_db
from schemas import UserCreate, UserUpdate, RecordCreate, RecordUpdate, RepmaxCreate, RepmaxUpdate, WorkoutCreate, WorkoutUpdate, ExerciseCreate, ExerciseUpdate, CategoryCreate, WorkoutExerciseCreate, WorkoutExerciseResponse, WorkoutExerciseUpdate, UserResponse, ExerciseResponse, WorkoutResponse, RecordResponse, RepmaxResponse, CategoryResponse
from psycopg2.errors import IntegrityError,ForeignKeyViolation

app = FastAPI()

# Home


@app.get("/")
def get_status():
    """
    Confirms that we are up and running
    """
    return "Running on localhost:8000..."

#                                                        Users Endpoints


@app.get("/users/{user_id}", status_code=200, response_model = UserResponse)
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


@app.get("/users", status_code=200, response_model=List[UserResponse])
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
                                user.weight, user.user_record_id, user.height)
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

#                                                   Records Endpoints


@app.get("/records/{user_id}", status_code=200, response_model=RecordResponse)
def get_record(user_id: int):
    """
    Returns records by user ID

    Raises exception if user is not found
    """
    con = get_connection()
    record = get_record_db(con, user_id)
    if record:
        return record
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/records", status_code=200, response_model=List[RecordResponse])
def get_records():
    """
    Returns a list of all users
    """
    con = get_connection()
    return get_records_db(con)


@app.post("/records", status_code=status.HTTP_201_CREATED)
def create_record(record: RecordCreate, con: Any = Depends(get_connection)):
    """
    Creates a record

    Raises exception if record already exists.
    Also raises exception if something went wrong when creating the record
    """
    try:
        result = create_record_db(
            con, record.workout_id, record.user_id, record.record_time)
        if result:
            return {'message': f'Record created sucessfully with id: {result}'}
        raise HTTPException(
            detail='Record not created properly', status_code=400)
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="Record already exists.")


@app.put('/records/{record_id}', status_code=status.HTTP_200_OK)
def update_record(record_id: int, record_time: RecordUpdate, con: Any = Depends(get_connection)):
    """
    Updates record time in a user by ID

    Raises exception if no input was provided.

    """
    try:
        update_records_db(con, record_id, record_time)
        return {'message': 'Record updated successfully'}

    except HTTPException:
        raise HTTPException


@app.delete('/records/{record_id}')
def delete_record(record_id: int, con: Any = Depends(get_connection)):
    """
    Deletes a user by ID

    Raises exception if user could not be found
    """
    result = delete_record_db(con, record_id)
    if result:
        return {'message': f'Record with id {result['record_id']} deleted'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


#                                                   Exercises Endpoints


@app.get("/exercises/{exercise_id}", status_code=200, response_model=ExerciseResponse)
def get_exercise(exercise_id: int):
    """
    Returns a user by ID

    Raises exception if user is not found
    """
    con = get_connection()
    exercise = get_exercise_db(con, exercise_id)
    if exercise:
        return exercise
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/exercises", status_code=200, response_model=List[ExerciseResponse])
def get_exercises():
    """
    Returns a list of all exercises
    """
    con = get_connection()
    return get_exercises_db(con)


@app.post("/exercises", status_code=status.HTTP_201_CREATED)
def create_exercise(exercise: ExerciseCreate, con: Any = Depends(get_connection)):
    """
    Creates an exercise

    Raises exception if exercise already exists.
    Also raises exception if something went wrong when creating the user
    """
    try:
        result = create_exercise_db(con, exercise.name, exercise.weight,
                                    exercise.repmax_id, exercise.category_id, exercise.base_exercise)
        if result:
            return {'message': f'Exercise created sucessfully with id: {result}'}
        raise HTTPException(
            detail='Exericse not created properly', status_code=400)
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="Exercise already exists.")


@app.patch('/exercises/{exercise_id}', status_code=status.HTTP_200_OK)
def update_exercise(exercise_id: int, exercise: ExerciseUpdate, con: Any = Depends(get_connection)):
    """
    Updates one or more fields in an exercise by ID

    Raises exception if exercise already exists, or if no input was provided.

    """
    try:
        # Extract fields from ExerciseUpdate and iterate over them
        # Only include fields that are set
        update_data = exercise.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No fields provided for update.")

        for column, value in update_data.items():
            # The function gets called for every row to enable the option to update several rows at once
            update_user_db(con, exercise_id, update_column=column,
                           update_value=value)

        return {'message': 'Exercise updated successfully'}

    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="Exercise already exists.")


@app.delete('/exercises/{exercise_id}')
def delete_exercise(exercise_id: int, con: Any = Depends(get_connection)):
    """
    Deletes a exercise by ID

    Raises exception if exercise could not be found
    """
    result = delete_exercise_db(con, exercise_id)
    if result:
        return {'message': f'Exercise with id {result['exercise_id']} deleted'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


#                                                   Workouts Endpoints


@app.get("/workouts/{workout_id}", status_code=200, response_model=WorkoutResponse)
def get_workout(workout_id: int):
    """
    Returns a workout by ID

    Raises exception if workout is not found
    """
    con = get_connection()
    workout = get_workout_db(con, workout_id)
    if workout:
        return workout
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/workouts", status_code=200, response_model=List[WorkoutResponse])
def get_workout():
    """
    Returns a list of all workouts
    """
    con = get_connection()
    return get_workouts_db(con)


@app.post("/workouts", status_code=status.HTTP_201_CREATED)
def create_user(workout: WorkoutCreate, con: Any = Depends(get_connection)):
    """
    Creates a workout

    Raises exception if workout already exists.
    Also raises exception if something went wrong when creating the workout
    """
    try:
        result = create_workout_db(con, workout.name, workout.timecap,
                                   workout.record_id, workout.for_kids)
        if result:
            return {'message': f'Workout created sucessfully with id: {result}'}
        raise HTTPException(
            detail='Workout not created properly', status_code=400)
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="Workout already exists.")


@app.patch('/workouts/{workout_id}', status_code=status.HTTP_200_OK)
def update_workout(workout_id: int, workout: WorkoutUpdate, con: Any = Depends(get_connection)):
    """
    Updates one or more fields in a workout by ID

    Raises exception if workout already exists, or if no input was provided.

    """
    try:
        # Extract fields from WorkoutUpdate and iterate over them
        # Only include fields that are set
        update_data = workout.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No fields provided for update.")

        for column, value in update_data.items():
            # The function gets called for every row to enable the option to update serveral rows at once
            update_workout_db(con, workout_id, update_column=column,
                              update_value=value)

        return {'message': 'Workout updated successfully'}

    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="Workout already exists.")


@app.delete('/workouts/{workout_id}')
def delete_workout(workout_id: int, con: Any = Depends(get_connection)):
    """
    Deletes a workout by ID

    Raises exception if workout could not be found
    """
    result = delete_workout_db(con, workout_id)
    if result:
        return {'message': f'Workout with id {result['workout_id']} deleted'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


#                                                   Repmax Endpoints

@app.get("/repmaxs", status_code=200, response_model=List[RepmaxResponse])
def get_repmaxs():
    """
    Returns a list of all repmaxs
    """
    con = get_connection()
    return get_repmaxs_db(con)


@app.post("/repmaxs", status_code=status.HTTP_201_CREATED)
def create_repmax(repmax: RepmaxCreate, con: Any = Depends(get_connection)):
    """
    Creates a repmax

    Raises exception if repmax already exists.
    Also raises exception if something went wrong when creating the user
    """
    try:
        result = create_repmax_db(
            con, repmax.exercise_id, repmax.user_id, repmax.weight)
        if result:
            return {'message': f'Repmax created sucessfully with id: {result}'}
        raise HTTPException(
            detail='Repmax not created properly', status_code=400)
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="Repmax already exists.")


@app.patch('/repmaxs/{repmax_id}', status_code=status.HTTP_200_OK)
def update_repmax(repmax_id: int, repmax: RepmaxUpdate, con: Any = Depends(get_connection)):
    """
    Updates one or more fields in a repmaxby ID

    Raises exception if repmax already exists, or if no input was provided.

    """
    try:
        # Extract fields from RepmaxUpdate and iterate over them
        # Only include fields that are set
        update_data = repmax.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No fields provided for update.")

        for column, value in update_data.items():
            # The function gets called for every row to enable the option to update serveral rows at once
            update_repmax_db(con, repmax_id, update_column=column,
                             update_value=value)

        return {'message': 'Repmax updated successfully'}

    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="Repmax already exists.")


@app.delete('/repmaxs/{repmax_id}')
def delete_repmax(repmax_id: int, con: Any = Depends(get_connection)):
    """
    Deletes a repmax by ID

    Raises exception if user could not be found
    """
    result = delete_repmax_db(con, repmax_id)
    if result:
        return {'message': f'Repmax with id {result['repmax_id']} deleted'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


#                                                   Categories Endpoints


@app.get("/categories", status_code=200, response_model=List[CategoryResponse])
def get_categories():
    """
    Returns a list of all categories
    """
    con = get_connection()
    return get_categories_db(con)


@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, con: Any = Depends(get_connection)):
    """
    Creates a category

    Raises exception if category already exists.
    Also raises exception if something went wrong when creating the category
    """
    try:
        result = create_category_db(con, category.name)
        if result:
            return {'message': f'Category created sucessfully with id: {result}'}
        raise HTTPException(
            detail='Category not created properly', status_code=400)
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="Category already exists.")


@app.delete('/categories/{category_id}')
def delete_category(user_id: int, con: Any = Depends(get_connection)):
    """
    Deletes a category by ID

    Raises exception if category could not be found
    """
    result = delete_category_db(con, user_id)
    if result:
        return {'message': f'Category with id {result['category_id']} deleted'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


#                               Workout_exercises Endpoints


@app.get("/workout_exercises", response_model=List[WorkoutExerciseResponse], status_code=200)
def get_workout_exercises(con: Any = Depends(get_connection)):
    """
    Fetches all workout-exercise relationships
    """
    try:
        workout_exercises = get_workout_exercises_db(con)
        if not workout_exercises:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No workout-exercise relationships found."
            )
        return workout_exercises
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching workout-exercise relationships: {str(e)}"
        )



@app.get("/workout_exercises/{id}", response_model=WorkoutExerciseResponse, status_code=200)
def get_workout_exercise(id: int, con: Any = Depends(get_connection)):
    """
    Fetches a single workout-exercise relationship by ID
    """
    try:
        workout_exercise = get_workout_exercises_by_workout_id_db(con, id)
        if not workout_exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workout-Exercise relationship with ID {id} not found."
            )
        return workout_exercise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching the workout-exercise relationship: {str(e)}"
        )



@app.post("/workout_exercises", response_model=dict, status_code=201)
def create_workout_exercise(workout_exercise: WorkoutExerciseCreate, con: Any = Depends(get_connection)):
    """
    Creates a new workout-exercise relationship
    """
    try:
        result_id = create_workout_exercise_db(con, workout_exercise.workout_id, workout_exercise.exercise_id)
        return {"message": f"Workout-Exercise relationship created successfully with ID {result_id}"}
    except ForeignKeyViolation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid workout_id or exercise_id provided."
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Duplicate workout-exercise relationship detected."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the workout-exercise relationship: {str(e)}"
        )



@app.patch("/workout_exercises/{workout_exercise_id}")
def update_workout_exercise(workout_exercise_id: int, workout_exercise: WorkoutExerciseUpdate, con: Any = Depends(get_connection)):
    """
    Updates one or more fields in a workout_exercises by ID

    Raises exception if no input was provided.

    """
    update_data = workout_exercise.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="No fields provided for update")

    for column, value in update_data.items():
        update_workout_exercise_db(con, workout_exercise_id, column, value)

    return {"message": "Workout exercise updated successfully"}


@app.delete("/workout_exercises/{id}")
def delete_workout_exercise(id: int, con: Any = Depends(get_connection)):
    """
    Deletes a workout-exercise relationship by ID
    """
    try:
        result = delete_workout_exercise_db(con, id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workout-Exercise relationship with ID {id} not found."
            )
        return {"message": f"Workout-Exercise relationship with ID {id} deleted successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the workout-exercise relationship: {str(e)}"
        )
