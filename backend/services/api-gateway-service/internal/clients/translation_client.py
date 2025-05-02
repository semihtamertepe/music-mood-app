import aiohttp
import os
from typing import Dict, Any

TRANSLATION_SERVICE_URL = os.getenv("TRANSLATION_SERVICE_URL", "http://localhost:8003")

async def translate_text(text: str, token: str) -> Dict[str, str]:
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{TRANSLATION_SERVICE_URL}/translate/tr-to-en",
            json={"text": text},
            headers={"Authorization": f"Bearer {token}"}
        ) as response:
            if response.status != 200:
                error_detail = await response.json()
                raise Exception(error_detail.get("detail", "Translation failed"))
            return await response.json() 