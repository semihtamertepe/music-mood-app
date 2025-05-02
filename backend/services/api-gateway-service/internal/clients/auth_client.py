import aiohttp
import os
from typing import Optional, Dict, Any, List

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")

async def verify_token(token: str) -> Dict[str, Any]:
    """
    Auth service ile token doğrulaması yapar
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{AUTH_SERVICE_URL}/auth/verify-token",
            json={"token": token}
        ) as response:
            if response.status != 200:
                error_detail = await response.json()
                raise Exception(error_detail.get("detail", "Token verification failed"))
            result = await response.json()
            if not result.get("verify"):
                raise Exception("Token verification failed")
            return result

async def get_user_info(token: str) -> Dict[str, Any]:
    """
    Auth service'den kullanıcı bilgilerini alır
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{AUTH_SERVICE_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        ) as response:
            if response.status != 200:
                error_detail = await response.json()
                raise Exception(error_detail.get("detail", "Failed to get user info"))
            return await response.json()

async def register_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{AUTH_SERVICE_URL}/auth/register",
            json=user_data
        ) as response:
            if response.status != 200:
                error_detail = await response.json()
                raise Exception(error_detail.get("detail", "Registration failed"))
            return await response.json()

async def login_user(credentials: Dict[str, str]) -> Dict[str, str]:
    form_data = {
        "username": credentials["username"],
        "password": credentials["password"]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{AUTH_SERVICE_URL}/auth/login",
            data=form_data
        ) as response:
            if response.status != 200:
                error_detail = await response.json()
                raise Exception(error_detail.get("detail", "Login failed"))
            return await response.json()

async def get_user_info(token: str) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{AUTH_SERVICE_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        ) as response:
            if response.status != 200:
                error_detail = await response.json()
                raise Exception(error_detail.get("detail", "Failed to get user info"))
            return await response.json()

async def get_user_preferences(username: str) -> Dict[str, Optional[str]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{AUTH_SERVICE_URL}/auth/user/preferences",
            params={"username": username},
            headers={"Content-Type": "application/json"}
        ) as response:
            if response.status != 200:
                error_detail = await response.json()
                raise Exception(error_detail.get("detail", "Failed to get user preferences"))
            return await response.json()

async def decode_access_token(token: str) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{AUTH_SERVICE_URL}/auth/decode-token",
            json={"token": token}
        ) as response:
            if response.status != 200:
                error_detail = await response.json()
                raise Exception(error_detail.get("detail", "Failed to decode token"))
            return await response.json()

async def get_users():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{AUTH_SERVICE_URL}/auth/users") as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Auth service error {response.status}: {text}")
            return await response.json()

