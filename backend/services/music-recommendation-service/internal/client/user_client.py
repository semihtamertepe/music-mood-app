import httpx
import os

API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8000")

async def get_user_profile(username: str, token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_GATEWAY_URL}/api/auth/users/{username}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        response.raise_for_status()
        return response.json()


async def fetch_user_info(username: str, token: str) -> dict:
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(
            f"{API_GATEWAY_URL}/api/auth/user/preferences",
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        return response.json()