from pydantic import BaseModel

class MusicRecommendationResponse(BaseModel):
    room_id: str
    music_name: str
    artist: str
    sentiment_label: str
    genre: str
    timestamp: str

   
class MusicSentimentRequest(BaseModel):
    room_id: str
    
class MusicSentimentResponse(BaseModel):
    sentiment: str
    recommended_music: str