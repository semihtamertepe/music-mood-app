from fastapi import APIRouter, HTTPException, Header, Query
from internal.service.recommendation_service import recommend_music

router = APIRouter()

@router.post("/predict")
async def recommend_music_endpoint(room_id: str = Query(..., title="Room ID"), authorization: str = Header(...)):
    """
    Room ID'ye göre müzik önerisi yapar.
    Kullanıcı token'ı header Authorization: Bearer TOKEN şeklinde gelmeli.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    
    token = authorization.replace("Bearer ", "")

    recommendation = await recommend_music(room_id, token)
    if not recommendation:
        return {"message": "No music recommendation available"}
    return recommendation
