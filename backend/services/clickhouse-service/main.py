from fastapi import FastAPI
from internal.router.room_router import router
from internal.database.clickhouse import ClickHouseDB
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

db = ClickHouseDB()

@app.on_event("startup")
async def startup_event():
    db.create_database_and_tables()

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Clickhouse Service is Running"}
