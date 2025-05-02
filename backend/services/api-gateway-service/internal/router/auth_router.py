from fastapi import APIRouter, Depends, HTTPException
from internal.clients.auth_client import (
    register_user,
    login_user,
    get_user_info,
    get_user_preferences,
    decode_access_token,
    get_users
)
from internal.schemas.auth_schemas import UserCreate, UserLogin, UserResponse, UserPreferences, Token, VerifyTokenRequest, VerifyTokenResponse
from typing import List

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    try:
        return await register_user(user.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    try:
        return await login_user(user.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(token: str):
    try:
        return await get_user_info(token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/preferences", response_model=UserPreferences)
async def get_preferences(username: str):
    try:
        return await get_user_preferences(username)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/verify-token", response_model=VerifyTokenResponse)
async def verify_token_endpoint(request: VerifyTokenRequest):
    payload = await decode_access_token(request.token)
    if payload:
        return payload
    else:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/users", response_model=List[UserResponse])
async def get_users_router():
    return await get_users()
