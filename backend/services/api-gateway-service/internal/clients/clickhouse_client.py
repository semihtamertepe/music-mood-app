import os
import httpx

CLICKHOUSE_SERVICE_URL = os.getenv("CLICKHOUSE_SERVICE_URL", "http://localhost:8005")

async def get_or_create_room(username1: str, username2: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CLICKHOUSE_SERVICE_URL}/api/get_or_create_room",
            params={"username1": username1, "username2": username2},
            timeout=10
        )
        response.raise_for_status()
        return response.json()


async def get_messages(room_id: str, limit: int = 50, offset: int = 0):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CLICKHOUSE_SERVICE_URL}/api/get_messages",
            params={"room_id": room_id, "limit": limit, "offset": offset},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
async def get_users_by_room(room_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CLICKHOUSE_SERVICE_URL}/api/get_room_users",
            params={"room_id": room_id},
            timeout=10
        )
        response.raise_for_status()
        return response.json()