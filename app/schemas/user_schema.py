from pydantic import BaseModel, ConfigDict
from typing import Literal


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


class GeminiResponse(BaseModel):
    category: str
    score: float
    summary: str
    sentiment: Literal["positive", "negative", "neutral"]
