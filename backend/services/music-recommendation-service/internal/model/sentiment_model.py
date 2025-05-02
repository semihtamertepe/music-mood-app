import joblib
import os

MODEL_PATH = os.getenv("SENTIMENT_MODEL_PATH", "internal/model/sentiment_model.pkl")

class SentimentModel:
    def __init__(self):
        self.model = None

    def load(self):
        self.model = joblib.load(MODEL_PATH)
        print("Sentiment Model loaded!")

    def predict(self, text):
        return self.model.predict([text])[0]

sentiment_model = SentimentModel()
