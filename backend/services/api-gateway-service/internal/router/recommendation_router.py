from fastapi import APIRouter, Header, HTTPException, Query
from internal.clients.recommendation_client import predict_sentiment_from_music_service
from internal.schemas.recommendation_schemas import MusicSentimentRequest

router = APIRouter(
    prefix="/api/music-recommendation",
    tags=["Music Recommendation"]
)

@router.post("/predict")
async def predict_music_sentiment(room_id: str = Query(..., title="Oda Kimliği"), authorization: str = Header(...)):
    try:
        token = authorization.replace("Bearer ", "")
        sentiment = await predict_sentiment_from_music_service(
            room_id=room_id,
            token=token
        )
        return sentiment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
