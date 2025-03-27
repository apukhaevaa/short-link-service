from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from database import get_db
import schemas, crud, auth
from datetime import datetime
from typing import List

router = APIRouter()

# Создание короткой ссылки
@router.post("/shorten", response_model=schemas.URLInfo)
def create_short_link(link: schemas.URLShorten, db: Session = Depends(get_db), user: schemas.User = Depends(auth.get_current_user)):
    try:
        url = crud.create_url(db, link, user_id=user.id if user else None)
        return url
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Перенаправление на оригинальный URL с возможностью возврата JSON
@router.get("/{short_code}")
def redirect(short_code: str, request: Request, db: Session = Depends(get_db)):
    url = crud.get_original_url(db, short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL не найдена или устарела")
    crud.increment_click(db, url)
    if "application/json" in request.headers.get("accept", ""):
        return {"original_url": url.original_url}
    return RedirectResponse(url.original_url)

'''
# Удаление короткой ссылки
@router.delete("/{short_code}", response_model=schemas.URLInfo)
def delete_link(short_code: str, db: Session = Depends(get_db), user: schemas.User = Depends(auth.get_current_user)):
    url = crud.delete_url(db, short_code, user.id)
    if not url:
        raise HTTPException(status_code=404, detail="URL не найдена или доступ запрещён")
    return url
'''

'''
@router.delete("/{short_code}", response_model=schemas.URLInfo)
def delete_link(short_code: str, db: Session = Depends(get_db), user: schemas.User = Depends(auth.get_current_user)):
    # Допустим, проверка на роль "admin" уже сделана или не нужна
    url = crud.delete_url(db, short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL не найдена")
    return url'
'''

@router.delete("/{short_code}", response_model=schemas.URLInfo)
def delete_link(short_code: str, db: Session = Depends(get_db), user: schemas.User = Depends(auth.get_current_user)):
    url = crud.delete_url(db, short_code, user.id)
    if not url:
        raise HTTPException(status_code=404, detail="URL не найдена или доступ запрещён")
    return url

'''
@router.put("/{short_code}", response_model=schemas.URLInfo)
def update_link(short_code: str, new_url: schemas.URLBase, db: Session = Depends(get_db), user: schemas.User = Depends(auth.get_current_user)):
    updated_url = crud.update_url(db, short_code, new_url.original_url)
    if not updated_url:
        raise HTTPException(status_code=404, detail="URL не найдена")
    return updated_url'
'''

'''
@router.put("/{short_code}", response_model=schemas.URLInfo)
def update_link(short_code: str, new_url: schemas.URLBase, db: Session = Depends(get_db), user: schemas.User = Depends(auth.get_current_user)):
    normalized_url = new_url.original_url.rstrip("/") + "/"
    updated_url = crud.update_url(db, short_code, normalized_url)
    if not updated_url:
        raise HTTPException(status_code=404, detail="URL не найдена")
    return updated_url'
'''

@router.put("/{short_code}", response_model=schemas.URLInfo)
def update_link(short_code: str, new_url: schemas.URLBase, db: Session = Depends(get_db), user: schemas.User = Depends(auth.get_current_user)):
    updated_url = crud.update_url(db, short_code, new_url.original_url)
    if not updated_url:
        raise HTTPException(status_code=404, detail="URL не найдена")
    return updated_url

# Статистика по ссылке
@router.get("/{short_code}/stats", response_model=schemas.URLInfo)
def url_stats(short_code: str, db: Session = Depends(get_db)):
    url_info = crud.get_url_info(db, short_code)
    if not url_info:
        raise HTTPException(status_code=404, detail="URL не найдена")
    return url_info

# Поиск ссылки по оригинальному URL
@router.get("/search/", response_model=List[schemas.URLInfo])
def search_links(original_url: str = Query(...), db: Session = Depends(get_db)):
    urls = crud.search_url(db, original_url)
    if not urls:
        raise HTTPException(status_code=404, detail="URL не найдены")
    return urls

# Получение всех устаревших ссылок
@router.get("/expired/", response_model=List[schemas.URLInfo])
def get_expired_links(db: Session = Depends(get_db)):
    urls = crud.get_expired_urls(db)
    return urls

# Создание публичной короткой ссылки
@router.post("/public", response_model=schemas.URLInfo)
def create_public_short_link(link: schemas.URLShorten, project: str = None, db: Session = Depends(get_db)):
    url = crud.create_public_url(db, link, project)
    return url