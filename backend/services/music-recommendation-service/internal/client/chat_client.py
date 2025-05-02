import httpx
import os

API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8000")

async def get_last_messages(room_id: str, limit: int = 5):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_GATEWAY_URL}/api/chat/get_messages",
            params={"room_id": room_id, "limit": limit}
        )
        response.raise_for_status()
        return response.json()["messages"]
