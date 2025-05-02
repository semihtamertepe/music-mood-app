from fastapi import APIRouter, HTTPException
from internal.clients.translation_client import translate_text
from internal.schemas.translation_schemas import TranslationRequest, TranslationResponse


router = APIRouter(prefix="/api/translation", tags=["Translation"])

@router.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest, token: str):
    try:
        return await translate_text(request.text, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 