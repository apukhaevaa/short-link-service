# main.py
import auth
from fastapi import FastAPI
from database import Base, engine
# Если есть ваши роуты
from app.routes import admin, frontend
import app.routes.links as links

# Создаём таблицы
Base.metadata.create_all(bind=engine)

# Создаём приложение
app = FastAPI()

# Подключаем свои роуты
app.include_router(admin.router, prefix="/admin-panel", tags=["admin-panel"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(frontend.router, tags=["frontend"])
app.include_router(links.router, prefix="/links", tags=["links"])