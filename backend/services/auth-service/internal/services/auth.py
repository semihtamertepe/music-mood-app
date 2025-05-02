# services/auth-service/auth.py

from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from typing import Optional
from internal.models import User
from internal.schemas import UserCreate, UserLogin
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from internal.db import database
from fastapi.security import OAuth2PasswordRequestForm
# JWT için gizli anahtar ve ayarlar
SECRET_KEY = "7c43c6b678f4ad1d2e82b3279416dcab38e8e2e21d0fd446e77a9b202874b8cf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Bcrypt ayarları
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Şifre hashleme
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Şifre doğrulama
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT Token üretme
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# JWT Token çözümleme (isteğe bağlı kullanılacak)
def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

def verify_token_route(token: str, db: Session = Depends(database.get_db)):
    """
    Gelen token'ı doğrular.
    Geçerliyse {"verify": True}, değilse {"verify": False} döner.
    """
    try:
        payload = decode_access_token(token)
        if payload is None:
            return {"verify": False}

        return {"verify": True}
    except Exception:
        return {"verify": False}

def register(user: UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user.password)
    new_user = User(
        name=user.name,
        surname=user.surname,
        username=user.username,
        hashed_password=hashed_password,
        favorite_artist=user.favorite_artist,
        favorite_genre=user.favorite_genre
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    db_user = db.query(User).filter(User.username == form_data.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

def get_users(db: Session = Depends(database.get_db)):
    try:
        users = db.query(User).all()
        print("Users fetched:", users)
        return users
    except Exception as e:
        print("Exception in /users:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


