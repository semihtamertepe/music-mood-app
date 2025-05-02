import os
import pandas as pd
import numpy as np
import scipy.sparse as sp
from collections import Counter
from joblib import load
from internal.client.chat_client import get_last_messages
from internal.client.translation_client import translate_to_english
from internal.client.user_client import fetch_user_info
from internal.model.music_dataset_loader import music_dataset

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, 'model', 'sentiment_model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'model', 'tfidf_vectorizer.pkl')
ENCODER_PATH = os.path.join(BASE_DIR, 'model', 'sentiment_label_encoder.pkl')

model = load(MODEL_PATH)
tfidf_vectorizer = load(VECTORIZER_PATH)
label_encoder = load(ENCODER_PATH)

DATASET_PATH = os.path.join(BASE_DIR, 'model', 'music_sentiment_dataset.csv')
df = pd.read_csv(DATASET_PATH)

artist_list = sorted(df['Artist'].dropna().unique().tolist())
genre_list = sorted(df['Genre'].dropna().unique().tolist())

artist_to_int = {name: idx for idx, name in enumerate(artist_list)}
genre_to_int = {name: idx for idx, name in enumerate(genre_list)}

async def recommend_music(room_id: str, token: str):
    print(f"Oneri araniyor - Room ID: {room_id}")
    messages = await get_last_messages(room_id)
    if not messages:
        return None
    print(f"Mesajlar: {messages}")
    sentiments = []

    for msg in messages:
        text = msg["message"]
        sender = msg["sender"]

        try:
            user_info = await fetch_user_info(sender, token)
            favorite_artist = user_info.get("favorite_artist", "")
            favorite_genre = user_info.get("favorite_genre", "")
        except Exception:
            favorite_artist = ""
            favorite_genre = ""

        translated_text = await translate_to_english(text, token)
        text_tfidf = tfidf_vectorizer.transform([translated_text])

        artist_encoded = np.array([[artist_to_int.get(favorite_artist, 0)]])
        genre_encoded = np.array([[genre_to_int.get(favorite_genre, 0)]])

        other_features = np.hstack([artist_encoded, genre_encoded])
        other_sparse = sp.csr_matrix(other_features)

        X = sp.hstack([text_tfidf, other_sparse])

        y_pred = model.predict(X)
        sentiment_label = label_encoder.inverse_transform(y_pred)[0]
        sentiments.append(sentiment_label)

    dominant_sentiment = Counter(sentiments).most_common(1)[0][0]
    recommended_music = music_dataset.get_random_music_by_sentiment(dominant_sentiment)

    return {
        "sentiment": dominant_sentiment,
        "recommended_music": recommended_music
    }
