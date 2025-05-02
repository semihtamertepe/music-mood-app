# services/auth-service/models.py

from sqlalchemy import Column, Integer, String
from internal.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    favorite_artist = Column(String, nullable=True)
    favorite_genre = Column(String, nullable=True)
