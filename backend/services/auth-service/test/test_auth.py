import asyncio
import aiohttp
import pytest

API_GATEWAY_URL = "http://localhost:8000"

async def test_auth_flow():
    # Test user data
    test_user = {
        "name": "Test",
        "surname": "User",
        "username": "testuser",
        "password": "testpass123",
        "favorite_artist": "Test Artist",
        "favorite_genre": "Test Genre"
    }

    async with aiohttp.ClientSession() as session:
        # Test registration
        async with session.post(f"{API_GATEWAY_URL}/api/auth/register", json=test_user) as response:
            assert response.status == 200
            register_data = await response.json()
            assert "access_token" in register_data
            token = register_data["access_token"]

        # Test login
        async with session.post(
            f"{API_GATEWAY_URL}/api/auth/login",
            json={"username": test_user["username"], "password": test_user["password"]}
        ) as response:
            assert response.status == 200
            login_data = await response.json()
            assert "access_token" in login_data

        # Test get preferences
        async with session.get(
            f"{API_GATEWAY_URL}/api/auth/me/preferences",
            headers={"Authorization": f"Bearer {token}"}
        ) as response:
            assert response.status == 200
            preferences = await response.json()
            assert preferences["favorite_artist"] == test_user["favorite_artist"]
            assert preferences["favorite_genre"] == test_user["favorite_genre"]

        # Test update preferences
        new_preferences = {
            "favorite_artist": "New Artist",
            "favorite_genre": "New Genre"
        }
        async with session.put(
            f"{API_GATEWAY_URL}/api/auth/me/preferences",
            json=new_preferences,
            headers={"Authorization": f"Bearer {token}"}
        ) as response:
            assert response.status == 200
            updated_preferences = await response.json()
            assert updated_preferences["favorite_artist"] == new_preferences["favorite_artist"]
            assert updated_preferences["favorite_genre"] == new_preferences["favorite_genre"]

if __name__ == "__main__":
    asyncio.run(test_auth_flow()) 