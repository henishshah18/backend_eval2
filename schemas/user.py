#creating schemas for user model

'''
User model:
id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
username: Mapped[str] = mapped_column(String, unique=True, index=True)
email: Mapped[str] = mapped_column(String, unique=True, index=True)
password: Mapped[str] = mapped_column(String)
phone_number: Mapped[str] = mapped_column(String, nullable=True)
balance: Mapped[float] = mapped_column(default=0.00)
created_at: Mapped[str] = mapped_column(default="CURRENT_TIMESTAMP")
updated_at: Mapped[str] = mapped_column(default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

'''

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone_number: Optional[str] = None

class UserCreate(UserBase):
    password: str
    balance: Optional[float] = 0.00
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    balance: Optional[float] = None
    updated_at: Optional[datetime] = None
    class Config:
        orm_mode = True

class UserFetch(UserBase):
    id: int
    balance: float
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True

