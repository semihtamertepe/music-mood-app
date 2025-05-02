from fastapi import APIRouter
from internal.service.room_service import get_or_create_room, get_users_by_room
from internal.service.message_service import get_messages_by_room

router = APIRouter()

@router.get("/api/get_or_create_room")
async def get_or_create(username1: str, username2: str):
    room_id = await get_or_create_room(username1, username2)
    return {"room_id": room_id}

@router.get("/api/get_messages")
async def get_messages(room_id: str):
    messages = await get_messages_by_room(room_id)
    return {"messages": messages}

@router.get("/api/get_room_users")
async def get_room_users(room_id: str):
    users = await get_users_by_room(room_id)
    return {"users": users}

