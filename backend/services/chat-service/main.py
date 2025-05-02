from fastapi import FastAPI
from services.mqtt_client import mqtt_client
from services.kafka_producer import start_producer, stop_producer, send_message_to_kafka


app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await start_producer()
    await mqtt_client.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await mqtt_client.disconnect()
    await stop_producer()

@app.get("/")
async def root():
    return {"message": "Chat Service is running (MQTT listener mode)"}
