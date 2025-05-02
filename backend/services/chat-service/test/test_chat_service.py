import json
import time
import threading
from kafka import KafkaConsumer, KafkaAdminClient

# Config ayarları
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "chat/test_room"

KAFKA_SERVER = "localhost:9093"
KAFKA_TOPIC = "chat-messages"

# Test mesajı
test_message = {
    "room_id": "alice_bob",
    "sender": "alice",
    "receiver": "bob",
    "message": "Hello Bob, this is a test!",
    "timestamp": "2023-01-01 12:00:00"
}

# Kafka topic'lerini listeleyen fonksiyon
def list_kafka_topics():
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_SERVER)
        topics = admin_client.list_topics()
        print(f"📚 Kafka'da mevcut topicler: {topics}")
    except Exception as e:
        print(f"❌ Kafka topic listesi alınamadı: {e}")

# Kafka consumer açıp gelen mesajı kontrol eden fonksiyon
def kafka_listener(stop_event):
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_SERVER],
        auto_offset_reset='earliest',  # En baştan oku (test için)
        enable_auto_commit=True,
        group_id='test-consumer-group',
        value_deserializer=lambda x: x.decode('utf-8')
    )
    print("👂 Kafka dinleniyor...")
    for msg in consumer:
        print(f"✅ Kafka mesajı geldi: {msg.value}")
        try:
            data = json.loads(msg.value)
            if (data.get("room_id") == test_message["room_id"] and
                data.get("sender") == test_message["sender"] and
                data.get("receiver") == test_message["receiver"] and
                data.get("message") == test_message["message"]):
                print("🎯 Test başarılı: Mesaj doğru şekilde Kafka'ya iletildi!")
            else:
                print("⚠️ Test başarısız: Gelen mesaj beklenenden farklı.")
        except Exception as e:
            print(f"❌ Gelen mesaj JSON formatında değil: {e}")

        stop_event.set()
        break

    consumer.close()  # 🔥 Kafka consumer kapatılıyor

# MQTT üzerinden mesaj gönderen fonksiyon
import paho.mqtt.publish as publish

import paho.mqtt.client as mqtt

def mqtt_publisher():
    time.sleep(2)  # Kafka listener hazır olsun diye biraz bekle
    try:
        client = mqtt.Client()
        client.username_pw_set(
            username="mqttuser",
            password="strongpassword123"
        )
        client.connect("localhost", 1883, 60)
        client.loop_start()
        print("✅ MQTT bağlantısı kuruldu!")

        client.publish(
            topic=MQTT_TOPIC,
            payload=json.dumps(test_message),
            qos=1,
            retain=False
        )
        print(f"✅ MQTT'ye publish yapıldı: {test_message}")

        time.sleep(2)  # Mesajın gitmesi için biraz bekle

        client.loop_stop()
        client.disconnect()
        print("✅ MQTT bağlantısı kapatıldı!")

    except Exception as e:
        print(f"❌ MQTT publish hatası: {e}")



# Testi başlat
if __name__ == "__main__":
    try:
        print("🚀 Test başlıyor...")
        list_kafka_topics()

        stop_event = threading.Event()
        kafka_thread = threading.Thread(target=kafka_listener, args=(stop_event,))
        kafka_thread.start()

        mqtt_publisher()

        # Maksimum 10 saniye bekle, sonra otomatik kapat
        if not stop_event.wait(timeout=10):
            print("❌ Test başarısız: 10 saniye içinde Kafka'dan mesaj alınamadı.")

        kafka_thread.join()

    except KeyboardInterrupt:
        print("\n🛑 Test manuel olarak Ctrl+C ile durduruldu.")

    finally:
        print("🏁 Test tamamlandı.")
