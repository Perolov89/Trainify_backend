# Pydantic schemas are used to validate data that you receive, or to make sure that whatever data

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

#                                                               User


class UserCreate(BaseModel):
    password: str= Field(max_length=100)
    name: str = Field(max_length=250)
    weight: int
    user_record_id: Optional[int]
    height: Optional[int]



class UserUpdate(BaseModel):
    password: Optional[str] = Field(None)
    name: Optional[str] = Field(None, max_length=250)
    weight: Optional[int] = Field(None)
    user_record_id: Optional[int] = Field(None)
    height: Optional[int] = Field(None)



class UserResponse(BaseModel):
    id: int
    password: str= Field(max_length=100)
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
    weight: Optional[int] = Field(None)
    repmax_id: Optional[int] = Field(None)
    primary_muscle: Optional[str] = Field(None, max_length=100)
    secondary_muscle: Optional[str] = Field(None, max_length=100)
    category_id: Optional[int] = Field(None)
    base_exercise: Optional[bool]

class ExerciseResponse(BaseModel):
    id: int
    name: str = Field(max_length=250)
    weight: int
    repmax_id: int
    primary_muscle: Optional[str]
    secondary_muscle: Optional[str]
    category_id: int
    base_exercise: bool

#                                                              Record
class RecordCreate(BaseModel):
    workout_id: int
    user_id: int
    record_time: datetime

class RecordUpdate(BaseModel):
    workout_id: Optional[int] = Field(None)
    user_id: Optional[int] = Field(None)
    record_time: Optional[datetime] = Field(None)

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
    exercise_id: Optional[int] = Field(None)
    user_id: Optional[int] = Field(None)
    weight: Optional[int] = Field(None)

class RepmaxResponse(BaseModel):
    id: int
    exercise_id: int
    user_id: int
    weight: int


#                                                            Workout
class WorkoutCreate(BaseModel):
    name: str = Field(max_length=250)
    timecap: Optional[int]
    record_id: int
    exercise_id: int

class WorkoutUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=250)
    timecap: Optional[int] = Field(None)
    record_id: Optional[int] = Field(None)
    exercise_id: Optional[int] = Field(None)

class WorkoutResponse(BaseModel):
    id: int
    name: str = Field(max_length=250)
    timecap: Optional[int]
    record_id: int
    exercise_id: int


#                                                           Category
class CategoryCreate(BaseModel):
    name: str = Field(max_length=100)

class CategoryResponse(BaseModel):
    id: int
    name: str = Field(max_length=100)
