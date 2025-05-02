import asyncio
import numpy as np
import scipy.sparse as sp
from joblib import load
import os
import httpx

# Load model, vectorizer and label encoder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'internal', 'model', 'sentiment_model.pkl')
VECTOR_PATH = os.path.join(BASE_DIR, 'internal', 'model', 'tfidf_vectorizer.pkl')
ENCODER_PATH = os.path.join(BASE_DIR, 'internal', 'model', 'sentiment_label_encoder.pkl')

model = load(MODEL_PATH)
tfidf_vectorizer = load(VECTOR_PATH)
label_encoder = load(ENCODER_PATH)

artist_list = ["Adele", "Drake", "BTS", "Taylor Swift"]
genre_list = ["Pop", "Hip-Hop", "Rock", "EDM"]

artist_to_int = {name: idx for idx, name in enumerate(artist_list)}
genre_to_int = {name: idx for idx, name in enumerate(genre_list)}

API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8000")

async def translate_to_english(text: str, token: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_GATEWAY_URL}/api/translation/translate",
            params={"token": token},  # Değişiklik burada
            json={"text": text},
            timeout=15
        )
        response.raise_for_status()
        return response.json()["translated_text"]


def predict_sentiment(text, favorite_artist="", favorite_genre=""):
    text_tfidf = tfidf_vectorizer.transform([text])
    
    artist_encoded = np.array([[artist_to_int.get(favorite_artist, 0)]])
    genre_encoded = np.array([[genre_to_int.get(favorite_genre, 0)]])
    
    other_features = np.hstack([artist_encoded, genre_encoded])
    other_sparse = sp.csr_matrix(other_features)
    
    X = sp.hstack([text_tfidf, other_sparse])
    
    y_pred = model.predict(X)
    
    sentiment_label = label_encoder.inverse_transform(y_pred)[0]
    return sentiment_label

# Ana test çalıştırıcısı
async def main():
    text = "Bugün çok üzgünüm, bu kadar kötü bir gün yaşamışım."
    favorite_artist = "Kanye West"
    favorite_genre = "Hip-Hop"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzQ1ODQxMzc5fQ.OU8nbUZ52x_CF_NwU7SJ9b4d6X5PL5teJoJAoMcSfEQ"  # testi çalıştırmak için token gerekli

    print("Çeviri yapılıyor...")
    translated_text = await translate_to_english(text, token)
    print(f"İngilizce Çeviri: {translated_text}")

    print("🔍 Predict ediliyor...")
    result = predict_sentiment(
        text=translated_text, 
        favorite_artist=favorite_artist, 
        favorite_genre=favorite_genre
    )
    print(f"Predicted Sentiment: {result}")

# Çalıştır
if __name__ == "__main__":
    asyncio.run(main())
