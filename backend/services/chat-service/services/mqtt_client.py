import os
import asyncio
import json
from paho.mqtt import client as mqtt
from services.kafka_producer import start_producer, stop_producer, send_message_to_kafka

import os
import asyncio
import json
from contextlib import AsyncExitStack
from aiomqtt import Client, MqttError
from services.kafka_producer import send_message_to_kafka

class MQTTClient:
    def __init__(self):
        self.broker = os.getenv("MQTT_BROKER", "localhost")
        self.port = int(os.getenv("MQTT_PORT", 1883))
        self.topic = os.getenv("MQTT_TOPIC", "chat/#")
        self.username = os.getenv("MQTT_USERNAME", "mqttuser")
        self.password = os.getenv("MQTT_PASSWORD", "strongpassword123")

    async def connect(self):
        async with AsyncExitStack() as stack:
            client = Client(
                hostname=self.broker,
                port=self.port,
                username=self.username,
                password=self.password
            )
            await stack.enter_async_context(client)
            
            print("MQTT Connected")
            await client.subscribe(self.topic)
            print(f"Subscribed to {self.topic}")

            async for message in client.messages:
                await self.on_message(message)

    async def on_message(self, message):
        try:
            payload = json.loads(message.payload.decode())
            print(f"MQTT Received: {payload}")
            await send_message_to_kafka(payload)  # Kafka'ya async gönderim
            print("Kafka'ya başarıyla gönderildi")
        except Exception as e:
            print(f"Hata: {str(e)}")

mqtt_client = MQTTClient()
