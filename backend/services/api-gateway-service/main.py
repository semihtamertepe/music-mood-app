from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from internal.router.clickhouse_router import router as clickhouse_router
from internal.router.auth_router import router as auth_router
from internal.router.recommendation_router import router as recommendation_router
from internal.router.translation_router import router as translation_router

app = FastAPI(title="API Gateway")

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clickhouse_router)
app.include_router(auth_router)
app.include_router(recommendation_router)
app.include_router(translation_router)

@app.get("/")
async def root():
    return {"message": "API Gateway is Running"}
