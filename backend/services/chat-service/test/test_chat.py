import asyncio
import aiohttp
import json
from datetime import datetime
import pytest

API_GATEWAY_URL = "http://localhost:8000"
CHAT_SERVICE_URL = "http://localhost:8002"

async def register_user(session: aiohttp.ClientSession, username: str, password: str) -> str:
    """Kullanıcı kaydı yapar ve token döndürür"""
    async with session.post(
        f"{API_GATEWAY_URL}/api/auth/register",
        json={"username": username, "password": password}
    ) as response:
        assert response.status == 200
        data = await response.json()
        return data["access_token"]

async def login_user(session: aiohttp.ClientSession, username: str, password: str) -> str:
    """Kullanıcı girişi yapar ve token döndürür"""
    async with session.post(
        f"{API_GATEWAY_URL}/api/auth/login",
        json={"username": username, "password": password}
    ) as response:
        assert response.status == 200
        data = await response.json()
        return data["access_token"]

async def send_message(session: aiohttp.ClientSession, token: str, message_data: dict) -> dict:
    """Mesaj gönderir"""
    async with session.post(
        f"{API_GATEWAY_URL}/api/chat/message",
        json=message_data,
        headers={"Authorization": f"Bearer {token}"}
    ) as response:
        assert response.status == 200
        return await response.json()

async def get_messages(session: aiohttp.ClientSession, token: str, sender: str, receiver: str) -> list:
    """Mesaj geçmişini getirir"""
    async with session.get(
        f"{API_GATEWAY_URL}/api/chat/messages/{sender}/{receiver}",
        headers={"Authorization": f"Bearer {token}"}
    ) as response:
        assert response.status == 200
        return await response.json()

async def test_chat_flow():
    """Chat akışını test eder"""
    async with aiohttp.ClientSession() as session:
        # İki test kullanıcısı oluştur
        user1 = {
            "username": "test_user1",
            "password": "testpass123"
        }
        user2 = {
            "username": "test_user2",
            "password": "testpass123"
        }
        
        # Kullanıcıları kaydet ve giriş yap
        token1 = await register_user(session, user1["username"], user1["password"])
        token2 = await register_user(session, user2["username"], user2["password"])
        
        # Test mesajları
        messages = [
            {
                "sender_username": user1["username"],
                "receiver_username": user2["username"],
                "content": "Merhaba!"
            },
            {
                "sender_username": user2["username"],
                "receiver_username": user1["username"],
                "content": "Selam!"
            },
            {
                "sender_username": user1["username"],
                "receiver_username": user2["username"],
                "content": "Nasılsın?"
            }
        ]
        
        # Mesajları gönder
        for message in messages:
            token = token1 if message["sender_username"] == user1["username"] else token2
            response = await send_message(session, token, message)
            print(f"Message sent: {response}")
            await asyncio.sleep(1)  # Mesajların işlenmesi için bekle
        
        # Mesaj geçmişini kontrol et
        messages_history = await get_messages(session, token1, user1["username"], user2["username"])
        print("\nMessage History:")
        for msg in messages_history:
            print(f"{msg['sender_username']}: {msg['content']} ({msg['timestamp']})")
        
        # Mesaj sayısını kontrol et
        assert len(messages_history) >= len(messages), "Not all messages were saved"

if __name__ == "__main__":
    asyncio.run(test_chat_flow()) 