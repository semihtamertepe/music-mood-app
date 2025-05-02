# services/auth-service/main.py

from fastapi import FastAPI
from internal.routes import auth
import internal.models
from internal.db.database import engine

internal.models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Auth Service",
    description="Kullanıcı kayıt, giriş ve kimlik doğrulama için mikroservis.",
    version="1.0.0"
)

# Auth routes ekleniyor
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Auth Service is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)