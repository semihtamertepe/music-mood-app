from fastapi import APIRouter, HTTPException, Header
from internal.services.translation import translate_text
from internal.schemas.translation_schemas import TranslationRequest, TranslationResponse
from internal.clients.auth_client import verify_token

router = APIRouter(prefix="/translate", tags=["Translation"])

@router.post("/tr-to-en", response_model=TranslationResponse)
async def translate_tr_to_en(request: TranslationRequest, authorization: str = Header(...)):
    """
    Gelen Authorization header içindeki Bearer Token'ı doğrular, 
    eğer geçerliyse çeviri yapar.
    """
    try:
        print(authorization)
        # Authorization: Bearer <token> -> sadece token'ı alıyoruz
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header format")

        token = authorization.replace("Bearer ", "")

        # Token doğrulaması API Gateway üzerinden
        verification_response = await verify_token(token)
        if not verification_response.get("verify"):
            raise HTTPException(status_code=401, detail="Token verification failed")

        # Token doğrulandıktan sonra çeviri yap
        translated_text = await translate_text(request.text)
        return {"translated_text": translated_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
