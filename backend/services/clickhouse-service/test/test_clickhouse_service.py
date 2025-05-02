import asyncio
import httpx

# ClickHouse Service adresi
CLICKHOUSE_SERVICE_URL = "http://localhost:8005"

async def test_get_or_create_room():
    print("🚀 Oda oluşturma veya getirme testi başlıyor...")

    params = {
        "username1": "alice",
        "username2": "bob"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CLICKHOUSE_SERVICE_URL}/api/get_or_create_room", params=params)
        assert response.status_code == 200, f"Hata: {response.text}"
        data = response.json()
        assert "room_id" in data, "room_id dönmedi!"
        print(f"✅ Oda başarıyla oluşturuldu veya getirildi: {data['room_id']}")
        return data["room_id"]

async def test_get_messages(room_id):
    print("🚀 Mesaj çekme testi başlıyor...")

    params = {
        "room_id": room_id,
        "limit": 10,
        "offset": 0
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CLICKHOUSE_SERVICE_URL}/api/get_messages", params=params)
        assert response.status_code == 200, f"Hata: {response.text}"
        data = response.json()
        assert "messages" in data, "messages listesi dönmedi!"
        print(f"✅ {len(data['messages'])} mesaj başarıyla çekildi.")

async def main():
    room_id = await test_get_or_create_room()
    await test_get_messages(room_id)

if __name__ == "__main__":
    asyncio.run(main())
