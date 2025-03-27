# models.py
from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Boolean
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)  # добавлена длина 50
    hashed_password = Column(String(128))       # добавлена длина 128

class URL(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String(2048), nullable=False)  # длина URL до 2048 символов
    short_code = Column(String(20), unique=True, index=True)  # короткий код до 20 символов
    custom_alias = Column(String(50), unique=True, nullable=True)  # до 50 символов
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    last_used = Column(DateTime)
    expires_at = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    project = Column(String(100), nullable=True)  # до 100 символов
    expired = Column(Boolean, default=False)