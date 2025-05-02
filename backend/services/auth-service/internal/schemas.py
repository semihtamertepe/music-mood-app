# services/auth-service/schemas.py

from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    surname: str
    username: str
    favorite_artist: Optional[str] = None
    favorite_genre: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None



class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    username: str
    favorite_artist: Optional[str] = None
    favorite_genre: Optional[str] = None

    class Config:
        orm_mode = True

class UserPreferences(BaseModel):
    favorite_artist: Optional[str] = None
    favorite_genre: Optional[str] = None

class VerifyTokenRequest(BaseModel):
    token: str