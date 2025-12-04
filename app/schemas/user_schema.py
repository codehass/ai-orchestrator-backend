from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserSchema(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
