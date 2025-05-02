import aiohttp
import os

GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8000")  # Gateway URL'sini ortamdan oku

async def verify_token(token: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{GATEWAY_URL}/api/auth/verify-token",
            json={"token": token}
        ) as response:
            if response.status != 200:
                error_detail = await response.json()
                raise Exception(error_detail.get("detail", "Token verification failed"))
            return await response.json()
