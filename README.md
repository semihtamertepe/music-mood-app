
# 🎵 Real-Time Emotion-Based Music Recommendation Chat App

This project is a full-stack system where users can message each other in real time and receive music recommendations based on the **emotional tone of their conversation**.

To ensure reliability under high traffic, EMQX MQTT broker is used instead of WebSockets, and microservices are connected via Kafka. My custom NLP model analyzes both users' emotional expressions and recommends a **mutual** track accordingly.

---

## 🚀 Key Features

- 💬 **Real-time chat** using MQTT protocol via EMQX (instead of WebSockets).
- 🧠 **Sentiment analysis model:** Trained on English text data, it analyzes conversation context.
- 🌐 **Microservice architecture:** Services are fully decoupled and communicate via Kafka.
- 📦 **ClickHouse Kafka Engine:** Messages are pushed to Kafka and automatically ingested into ClickHouse.
- 🌍 **Translation service:** Turkish input is translated to English before prediction.
- 🧠 **Persistent chat history:** Past messages are retrievable even after a session is closed.
- 🛡️ **API Gateway:** All frontend calls are securely routed through an API gateway.
- 🐳 **Dockerized architecture:** Fully runnable via `docker-compose`.

---

## 🧱 Microservices

- `auth-service`: JWT-based authentication
- `chat-service`: Consumes MQTT and pushes to Kafka
- `clickhouse-service`: Persists Kafka messages in ClickHouse
- `music-recommendation-service`: Predicts music from emotional context
- `translation-service`: Turkish to English translation
- `api-gateway`: Secure routing layer for all frontend communication

---

## ⚙️ Tech Stack

- **Frontend:** React (feature-based), Redux, SweetAlert
- **Backend:** FastAPI, aiohttp, SQLAlchemy
- **Streaming & Storage:** Kafka, EMQX, ClickHouse
- **Model:** Custom NLP Sentiment Model
- **Deployment:** Docker, Docker Compose

---

## 🔧 Getting Started

```bash
docker-compose up --build
```

> Note: Ensure model files and environment variables are loaded before start.

---

## 👨‍💻 Developer Note

This project was built to demonstrate the harmony of real-time data pipelines, multilingual NLP, and microservice communication. It's designed with a senior backend architecture mindset in mind.

---

# 🇹🇷 Gerçek Zamanlı Duygu Durumuna Göre Müzik Öneren Sohbet Uygulaması

Bu proje, kullanıcıların anlık olarak mesajlaşabildiği ve bu mesajların duygusal içeriğine göre özel müzik önerileri alabildiği tam yığın (full-stack) bir sistemdir.

Yüksek eş zamanlılıkta WebSocket bağlantılarının çökmesini önlemek için EMQX kullanılmış, mikroservis mimarisi ile ayrıştırılmış servisler Kafka ile birbirine bağlanmıştır. NLP modelim, konuşma geçmişini analiz ederek her iki kullanıcının duygu durumunu dikkate alarak aynı anda ikisi için de uygun bir müzik önerisi sunar.

---

## 🚀 Temel Özellikler

- 💬 **Gerçek zamanlı sohbet:** WebSocket yerine MQTT protokolü ile daha kararlı bağlantı (EMQX üzerinden).
- 🧠 **Duygu analizi modeli:** İngilizce veriyle eğitilmiş özel bir NLP model, konuşmalardan duygu çıkarımı yapar.
- 🌐 **Mikroservis mimarisi:** Servisler birbirinden ayrıdır, Kafka ile haberleşir.
- 📦 **ClickHouse Kafka Engine:** Sohbet mesajları Kafka’ya gönderilir, ClickHouse tarafından otomatik olarak toplanır.
- 🌍 **Dil çevirisi:** Türkçe gelen mesajlar `translation-service` ile İngilizceye çevrilerek modele aktarılır.
- 🧠 **Kalıcı geçmiş:** Uygulama kapansa bile geçmiş mesajlar ClickHouse üzerinden görüntülenebilir.
- 🛡️ **API Gateway:** Tüm sorgular güvenli bir şekilde `api-gateway` üzerinden yönlendirilir.
- 🐳 **Dockerize yapı:** Tüm sistem `docker-compose` ile ayağa kaldırılabilir.

---

## 🧱 Mikroservisler

- `auth-service`: JWT tabanlı kullanıcı yönetimi
- `chat-service`: MQTT mesajlarını Kafka'ya iletir
- `clickhouse-service`: Kafka'dan mesajları alır ve ClickHouse'a yazar
- `music-recommendation-service`: NLP model ile müzik tahmini
- `translation-service`: Türkçeden İngilizceye hızlı çeviri
- `api-gateway`: Tüm trafiğin geçtiği merkezi güvenli katman

---

## ⚙️ Teknolojiler

- **Frontend:** React (feature-based), Redux, SweetAlert
- **Backend:** FastAPI, aiohttp, SQLAlchemy
- **Veri Akışı:** Kafka, EMQX, ClickHouse
- **Model:** Custom NLP Sentiment Model
- **Dağıtım:** Docker, Docker Compose

---

## 🔧 Kurulum

```bash
docker-compose up --build
```

> Not: NLP model dosyası ve `.env` ayarları hazır olmalı.

---

