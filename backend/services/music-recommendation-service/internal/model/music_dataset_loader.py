# internal/model/music_dataset_loader.py

import pandas as pd
import os

DATASET_PATH = os.getenv("MUSIC_DATASET_PATH", "internal/model/music_sentiment_dataset.csv")

class MusicDataset:
    def __init__(self):
        self.df = None

    def load(self):
        self.df = pd.read_csv(DATASET_PATH)
        print("Music Dataset loaded!")

    def get_random_music_by_sentiment(self, sentiment_label):
        if self.df is None:
            raise ValueError("Music dataset is not loaded!")

        filtered = self.df[self.df['Sentiment_Label'] == sentiment_label]
        if not filtered.empty:
            return filtered.sample(1).iloc[0].to_dict()
        else:
            return None

    def get_artist_genre_dicts(self):
        if self.df is None:
            raise ValueError("Music dataset is not loaded!")

        artist_list = sorted(self.df['Artist'].dropna().unique().tolist())
        genre_list = sorted(self.df['Genre'].dropna().unique().tolist())

        artist_to_int = {artist: idx for idx, artist in enumerate(artist_list)}
        genre_to_int = {genre: idx for idx, genre in enumerate(genre_list)}

        return artist_to_int, genre_to_int

# Global nesne (servis başında yüklenir)
music_dataset = MusicDataset()
