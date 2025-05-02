# kafka_test_producer.py
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers=["localhost:9093"],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

message = {
    "room_id": "testroom",
    "sender": "testsender",
    "receiver": "testreceiver",
    "message": "Hello from test producer!"
}

print("➡️ Kafka'ya mesaj gönderiliyor...")
future = producer.send("chat-messages", message)
result = future.get(timeout=10)
print(f"✅ Kafka mesajı gönderildi: {result}")
producer.flush()
producer.close()
