from typing import List
import auth
import database
import schemas
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import models

router = APIRouter()

# Получаем сессию базы данных
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Только администратор
def admin_required(current_user: models.User = Depends(auth.get_current_user)):
    if current_user.username != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    return current_user


@router.get("/users", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db), current_user: models.User = Depends(admin_required)):
    users = db.query(models.User).all()
    return users


@router.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(admin_required)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user


@router.get("/urls", response_model=List[schemas.URLInfo])
def get_urls(db: Session = Depends(get_db), current_user: models.User = Depends(admin_required)):
    urls = db.query(models.URL).all()
    return urls


@router.delete("/urls/{short_code}", response_model=schemas.URLInfo)
def delete_url(short_code: str, db: Session = Depends(get_db), current_user: models.User = Depends(admin_required)):
    url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    db.delete(url)
    db.commit()
    return url


@router.get("/urls/stats", response_model=List[schemas.URLInfo])
def url_stats(db: Session = Depends(get_db), current_user: models.User = Depends(admin_required)):
    urls = db.query(models.URL).order_by(models.URL.clicks.desc()).all()
    return urls


