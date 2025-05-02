import asyncio
import aiohttp
import pytest

API_GATEWAY_URL = "http://localhost:8000"

async def test_translation_flow():
    async with aiohttp.ClientSession() as session:
        # Test messages
        test_messages = [
            "Merhaba, nasılsın?",
            "Bugün hava çok güzel.",
            "Müzik dinlemeyi sever misin?",
            "En sevdiğin şarkı nedir?",
            "Ben Türkçe konuşuyorum."
        ]

        for message in test_messages:
            async with session.post(
                f"{API_GATEWAY_URL}/api/translate/tr-to-en",
                json={"text": message}
            ) as response:
                assert response.status == 200
                translation = await response.json()
                print(f"\nOriginal: {message}")
                print(f"Translated: {translation['translated_text']}")

if __name__ == "__main__":
    asyncio.run(test_translation_flow()) 