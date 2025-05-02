import os
import aiohttp
from typing import Dict

MUSIC_RECOMMENDATION_SERVICE_URL = os.getenv("MUSIC_RECOMMENDATION_SERVICE_URL", "http://localhost:8006")

async def predict_sentiment_from_music_service(room_id: str, token: str) -> Dict[str, str]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{MUSIC_RECOMMENDATION_SERVICE_URL}/predict?room_id={room_id}",
                headers={"Authorization": f"Bearer {token}"}
            ) as response:
                response.raise_for_status()  # 4xx/5xx hatalarını yakala
                data = await response.json()
                
                # Eksik anahtarları kontrol et
                if "sentiment" not in data or "recommended_music" not in data:
                    raise ValueError("Geçersiz servis yanıtı")
                    
                return data
                
        except aiohttp.ClientResponseError as e:
            error_detail = await response.json()
            raise Exception(f"Music service error {e.status}: {error_detail}")
