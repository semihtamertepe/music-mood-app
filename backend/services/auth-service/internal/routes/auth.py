# services/auth-service/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from internal.models import User
from internal.schemas import UserResponse, UserLogin, UserCreate, Token, UserPreferences, VerifyTokenRequest
from internal.services import auth
from internal.db.database import get_db
from internal.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Kullanıcı kayıt
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = auth.register(user=user, db=db)
    # response modeline uygun dict dön
    return {
        "id": new_user.id,
        "name": new_user.name,
        "surname": new_user.surname,
        "username": new_user.username,
        "favorite_artist": new_user.favorite_artist,
        "favorite_genre": new_user.favorite_genre
    }


# Kullanıcı giriş
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token = auth.login(form_data=form_data, db=db)
    return token



# Token ile kullanıcı bilgisi al
@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
        return {
        "id": current_user.id,
        "name": current_user.name,
        "surname": current_user.surname,
        "username": current_user.username,
        "favorite_artist": current_user.favorite_artist,
        "favorite_genre": current_user.favorite_genre
    }

@router.get("/user/preferences", response_model=UserPreferences)
async def get_user_preferences(username: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"favorite_artist": user.favorite_artist, "favorite_genre": user.favorite_genre}



@router.post("/auth/verify-token")
async def verify_token_endpoint(request: VerifyTokenRequest):
    return auth.verify_token_route(request.token)

@router.post("/decode-token")
async def decode_token_endpoint(request: VerifyTokenRequest):
    return auth.verify_token_route(request.token)

@router.get("/users", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    return auth.get_users(db=db)


