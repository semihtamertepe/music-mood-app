# test/test_run.py

import asyncio
import os
import httpx

API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8000")

# Buraya login olmuş bir kullanıcıdan alınmış gerçek JWT token yazılacak
#token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzQ2MTc4ODYyfQ.WGcFAiqURIlkVuKLqj5cJDbtPXjk2JRQvJSZ4mn2UUg"


async def test_predict_sentiment():
    room_id = "alice_bob"

    async with httpx.AsyncClient(timeout=10) as client:
        
        login_res = await client.post(
            "http://localhost:8000/api/auth/login",
            json={"username": "tamer", "password": "1"}
        )
        print(login_res.json())
        token = login_res.json()["access_token"]
        predict_res = await client.post(
            "http://localhost:8000/api/music-recommendation/predict",
            params={"room_id": "alice_bob"},
            headers={"Authorization": f"Bearer {token}"}
        )
        print(predict_res.json())
        result = predict_res.json()
        print(f"🔧 Response Status: {predict_res.status_code}")
        print(f"🔧 Response Content: {predict_res.text}")
        print(f"🎯 API Gateway üzerinden tahmin sonucu: {result}")

if __name__ == "__main__":
    asyncio.run(test_predict_sentiment())
