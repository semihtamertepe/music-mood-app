from fastapi import FastAPI
from internal.router.recommendation_router import router as recommendation_router
from internal.model.sentiment_model import sentiment_model
from internal.model.music_dataset_loader import music_dataset

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    sentiment_model.load()
    music_dataset.load()

app.include_router(recommendation_router)

@app.get("/")
async def root():
    return {"message": "Music Recommendation Service is running"}
