from fastapi import APIRouter
from internal.clients.clickhouse_client import get_or_create_room, get_messages, get_users_by_room

router = APIRouter()

@router.get("/api/chat/get_or_create_room")
async def api_get_or_create_room(username1: str, username2: str):
    room_data = await get_or_create_room(username1, username2)
    return room_data

@router.get("/api/chat/get_messages")
async def api_get_messages(room_id: str, limit: int = 50, offset: int = 0):
    messages = await get_messages(room_id, limit, offset)
    return messages

@router.get("/api/chat/get_room_users")
async def api_get_room_users(room_id: str):
    users = await get_users_by_room(room_id)
    return users
