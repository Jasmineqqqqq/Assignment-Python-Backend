"""Pydantic schemas used for request/response bodies."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from .models import AppointmentStatus, UserRole


class UserBase(BaseModel):
    name: str = Field(..., example="Dr. John Doe")
    email: EmailStr = Field(..., example="john@example.com")
    role: UserRole = Field(..., example=UserRole.doctor)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, example="secret123")


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int | None = None


class AppointmentBase(BaseModel):
    doctor_id: int = Field(..., example=1)
    patient_id: int = Field(..., example=2)
    status: AppointmentStatus = Field(default=AppointmentStatus.pending)


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentRead(AppointmentBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True