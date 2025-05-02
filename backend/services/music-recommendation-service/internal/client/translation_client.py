import httpx
import os

API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8000")

async def translate_to_english(text: str, token: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_GATEWAY_URL}/api/translation/translate",
            params={"token": token},
            json={"text": text},
            timeout=15
        )
        response.raise_for_status()
        return response.json()["translated_text"]
