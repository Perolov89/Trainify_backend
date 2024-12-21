# Pydantic schemas are used to validate data that you receive, or to make sure that whatever data

from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime

#                                                               User


class UserCreate(BaseModel):
    username: str = Field(max_length=250)
    email: EmailStr
    password: str= Field(max_length=100)
    role_id: int
    realtor_id: Optional[int]


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=250)
    email: Optional[str] = Field(None)
    password: Optional[str] = Field(None)
    role_id: Optional[int] = Field(None)
    realtor_id: Optional[int] = Field(None)


class UserResponse(BaseModel):
    id: int
    username: str = Field(max_length=250)
    email: str
    password: str= Field(max_length=100)
    role_id: int
    realtor_id: int
