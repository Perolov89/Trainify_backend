# Pydantic schemas are used to validate data that you receive, or to make sure that whatever data

from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime

#                                                               User


class UserCreate(BaseModel):
    password: str= Field(max_length=100)
    name: str = Field(max_length=250)
    weight: int
    user_record_id: Optional[int]
    height: Optional[int]
    email: EmailStr


class UserUpdate(BaseModel):
    password: Optional[str] = Field(None)
    name: Optional[str] = Field(None, max_length=250)
    weight: Optional[int] = Field(None)
    user_record_id: Optional[int] = Field(None)
    height: Optional[int] = Field(None)
    email: Optional[str] = Field(None)


class UserResponse(BaseModel):
    id: int
    password: str= Field(max_length=100)
    name: str = Field(max_length=250)
    weight: int
    user_record_id: int
    height: int
    email: str
