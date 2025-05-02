from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    surname: str
    username: str
    password: str
    favorite_artist: Optional[str] = None
    favorite_genre: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    username: str
    favorite_artist: Optional[str] = None
    favorite_genre: Optional[str] = None

class UserPreferences(BaseModel):
    favorite_artist: Optional[str] = None
    favorite_genre: Optional[str] = None

class VerifyTokenRequest(BaseModel):
    token: str

class VerifyTokenResponse(BaseModel):
    verify: bool