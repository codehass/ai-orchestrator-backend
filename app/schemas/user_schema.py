from pydantic import BaseModel, ConfigDict
from typing import Literal
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserSchema(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class AnalyzeRequest(BaseModel):
    text: str
    is_public: bool


class GeminiResponse(BaseModel):
    category: str
    score: float
    summary: str
    title: str
    is_public: bool
    sentiment: Literal["positive", "negative", "neutral"]


class AnalyzeResponse(BaseModel):
    user_id: int
    id: int
    summary: str
    title: str
    is_public: bool
    sentiment: Literal["positive", "negative", "neutral"]
    category: str
    score: float
    created_at: datetime

    model_config = {"from_attributes": True}
