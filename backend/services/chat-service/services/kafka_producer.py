import os
import json
import asyncio
from kafka import KafkaProducer

producer = None

async def start_producer():
    global producer
    producer = KafkaProducer(
        bootstrap_servers=[os.getenv("KAFKA_SERVER", "localhost:9093")],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    print("Kafka producer started.")

async def stop_producer():
    global producer
    if producer:
        producer.close()
        print("Kafka producer stopped.")

async def send_message_to_kafka(message: dict):
    global producer
    print(f"send_message_to_kafka çağrıldı: {message}")
    
    if producer is None:
        print("Kafka producer NULL! Yeniden başlatılıyor...")
        await start_producer()
    
    if producer:
        def send_sync():
            future = producer.send(
                os.getenv("KAFKA_TOPIC", "chat-messages"),
                message
            )
            result = future.get(timeout=10)
            producer.flush()
            return result
        
        await asyncio.to_thread(send_sync)
        print(f"Kafka'ya mesaj basıldı (flushlandı): {message}")
    else:
        print("Kafka producer yine başlatılamadı!")


