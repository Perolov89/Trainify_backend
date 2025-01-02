# Pydantic schemas are used to validate data that you receive, or to make sure that whatever data

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

#                                                               User


class UserCreate(BaseModel):
    password: str = Field(max_length=100)
    name: str = Field(max_length=250)
    weight: int
    user_record_id: Optional[int] = None
    height: int



class UserUpdate(BaseModel):
    password: Optional[str] = Field(None, max_length=100)
    name: Optional[str] = Field(None, max_length=250)
    weight: Optional[int] = None
    user_record_id: Optional[int] = None
    height: Optional[int] = None



class UserResponse(BaseModel):
    id: int
    password: str = Field(max_length=100)
    name: str = Field(max_length=250)
    weight: int
    user_record_id: int
    height: int

#                                                            Exercise
class ExerciseCreate(BaseModel):
    name: str = Field(max_length=250)
    weight: int
    repmax_id: int
    primary_muscle: Optional[str] = Field(None, max_length=100)
    secondary_muscle: Optional[str] = Field(None, max_length=100)
    category_id: int
    base_exercise: bool

class ExerciseUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=250)
    weight: Optional[int] = None
    repmax_id: Optional[int] = None
    primary_muscle: Optional[str] = Field(None, max_length=100)
    secondary_muscle: Optional[str] = Field(None, max_length=100)
    category_id: Optional[int] = None
    base_exercise: Optional[bool] = None

class ExerciseResponse(BaseModel):
    id: int
    name: str = Field(max_length=250)
    weight: int
    repmax_id: int
    primary_muscle: str | None
    secondary_muscle: str | None
    category_id: int
    base_exercise: bool

#                                                              Record
class RecordCreate(BaseModel):
    workout_id: int
    user_id: int
    record_time: datetime

class RecordUpdate(BaseModel):
    workout_id: int | None = Field(...)
    user_id: int | None = Field(...)
    record_time: datetime | None = Field(...)

class RecordResponse(BaseModel):
    id: int
    workout_id: int
    user_id: int
    record_time: datetime


#                                                              Repmax
class RepmaxCreate(BaseModel):
    exercise_id: int
    user_id: int
    weight: int

class RepmaxUpdate(BaseModel):
    exercise_id: int | None = Field(...)
    user_id: int | None = Field(...)
    weight: int | None = Field(...)

class RepmaxResponse(BaseModel):
    id: int
    exercise_id: int
    user_id: int
    weight: int


#                                                            Workout
class WorkoutCreate(BaseModel):
    name: str = Field(max_length=250)
    timecap: int | None = Field(...)
    record_id: int
    exercise_id: int
    for_kids: bool

class WorkoutUpdate(BaseModel):
    name: str | None = Field(max_length=250)
    timecap: int | None = Field(...)
    record_id: int | None = Field(...)
    exercise_id: int | None = Field(...)
    for_kids: bool

class WorkoutResponse(BaseModel):
    id: int
    name: str = Field(max_length=250)
    timecap: int | None = Field(...)
    record_id: int
    exercise_id: int
    for_kids: bool


#                                                           Category
class CategoryCreate(BaseModel):
    name: str = Field(max_length=100)

class CategoryResponse(BaseModel):
    id: int
    name: str = Field(max_length=100)
