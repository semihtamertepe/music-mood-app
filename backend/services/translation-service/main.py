from fastapi import FastAPI
from internal.router import translation_router

app = FastAPI(title="Translation Service")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # API Gateway'in adresini ekleyin
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(translation_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
