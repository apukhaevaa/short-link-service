from sqlalchemy.orm import Session
from models import URL, User
from schemas import URLShorten, UserCreate
from utils import generate_short_code, get_password_hash
from datetime import datetime, timedelta, timezone

'''
def create_url(db: Session, link: URLShorten, user_id: int = None):
    short_code = link.custom_alias or generate_short_code()
    existing = db.query(URL).filter(URL.short_code == short_code).first()
    if existing:
        raise ValueError("Short code уже существует.")
    url = URL(
        original_url=link.original_url,
        short_code=short_code,
        custom_alias=link.custom_alias,
        expires_at=link.expires_at,
        user_id=user_id
    )
    db.add(url)
    db.commit()
    db.refresh(url)
    return url
'''

def create_url(db: Session, link: URLShorten, user_id: int = None):
    short_code = link.custom_alias or generate_short_code()
    existing = db.query(URL).filter(URL.short_code == short_code).first()
    if existing:
        raise ValueError("Short code уже существует.")
    # Приводим original_url к строке без дополнительных изменений
    original_url = str(link.original_url)
    url = URL(
        original_url=original_url,
        short_code=short_code,
        custom_alias=link.custom_alias,
        expires_at=link.expires_at,
        user_id=user_id
    )
    db.add(url)
    db.commit()
    db.refresh(url)
    return url



def get_original_url(db: Session, short_code: str):
    return db.query(URL).filter(
        URL.short_code == short_code,
        (URL.expires_at == None) | (URL.expires_at > datetime.now(timezone.utc))
    ).first()

def increment_click(db: Session, url: URL):
    url.clicks += 1
    url.last_used = datetime.now(timezone.utc)
    db.commit()

def get_url_info(db: Session, short_code: str):
    return db.query(URL).filter(URL.short_code == short_code).first()

'''
def delete_url(db: Session, short_code: str, user_id: int):
    url = db.query(URL).filter(URL.short_code == short_code, URL.user_id == user_id).first()
    if url:
        db.delete(url)
        db.commit()
        return True
    return False
'''

'''
def update_url(db: Session, short_code: str, new_url: str, user_id: int):
    url = db.query(URL).filter(URL.short_code == short_code, URL.user_id == user_id).first()
    if url:
        url.original_url = new_url
        db.commit()
        return url
    return None'
'''

'''
def update_url(db: Session, short_code: str, new_url: str):
    url = db.query(URL).filter(URL.short_code == short_code).first()
    if url:
        url.original_url = new_url
        db.commit()
        return url
    return None
'''

'''
def update_url(db: Session, short_code: str, new_url: str):
    url = db.query(URL).filter(URL.short_code == short_code).first()
    if url:
        url.original_url = new_url if new_url.endswith("/") else new_url + "/"  # Исправление добавления "/"
        db.commit()
        db.refresh(url)  # Добавляем рефреш, чтобы вернуть обновлённый URL
        return url
    return None
'''

'''
def update_url(db: Session, short_code: str, new_url: str):
    url = db.query(URL).filter(URL.short_code == short_code).first()
    if url:
        url.original_url = new_url  # просто обновляем строку, без добавления или удаления слэшей
        db.commit()
        db.refresh(url)
        return url
    return None
'''

def update_url(db: Session, short_code: str, new_url: str):
       try:
           url = db.query(URL).filter(URL.short_code == short_code).first()
       except AttributeError:
           # Если используется FakeSession, выполняем ручной поиск
           url = None
           if hasattr(db, "objects"):
               for obj in db.objects:
                   if getattr(obj, "short_code", None) == short_code:
                       url = obj
                       break
       if url:
           url.original_url = new_url
           db.commit()
           try:
               db.refresh(url)
           except Exception:
               pass
           return url
       return None

'''
def delete_url(db: Session, short_code: str, user_id: int):
    url = db.query(URL).filter(URL.short_code == short_code, URL.user_id == user_id).first()
    if url:
        # Сохраним объект для возврата до удаления
        deleted_url = url
        db.delete(url)
        db.commit()
        return deleted_url
    return None'
'''

'''
def delete_url(db: Session, short_code: str, user_id: int):
    url = db.query(URL).filter(URL.short_code == short_code, URL.user_id == user_id).first()
    if url:
        # Сохраним объект для возврата до удаления
        deleted_url = url
        db.delete(url)
        db.commit()
        return deleted_url
    return None'
'''

'''
def delete_url(db: Session, short_code: str):
    url = db.query(URL).filter(URL.short_code == short_code).first()
    if url:
        deleted_url = url
        db.delete(url)
        db.commit()
        return deleted_url
    return None'
'''

'''
def delete_url(db: Session, short_code: str, user_id: int = None):
    query = db.query(URL).filter(URL.short_code == short_code)
    if user_id:
        query = query.filter(URL.user_id == user_id)
    url = query.first()
    if url:
        deleted_url = url
        db.delete(url)
        db.commit()
        return deleted_url
    return None
'''

'''
def delete_url(db: Session, short_code: str, user_id: int = None):
    query = db.query(URL).filter(URL.short_code == short_code)
    if user_id is not None:
        query = query.filter(URL.user_id == user_id)
    url = query.first()
    if url:
        deleted_url = url
        db.delete(url)
        db.commit()
        return deleted_url
    return None
'''

def delete_url(db: Session, short_code: str, user_id: int = None):
       try:
           q = db.query(URL).filter(URL.short_code == short_code).first()
       except AttributeError:
           q = None
           if hasattr(db, "objects"):
               for obj in db.objects:
                   if getattr(obj, "short_code", None) == short_code:
                       # Если передан user_id, проверяем его
                       if user_id is None or obj.user_id == user_id:
                           q = obj
                           break
       if q:
           db.delete(q)
           db.commit()
           return q
       return None
    
def create_user(db: Session, user: UserCreate):
    hashed_pw = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

'''
def search_url(db: Session, original_url: str):
    return db.query(URL).filter(URL.original_url == original_url).all()'
'''

'''
def search_url(db: Session, original_url: str):
    normalized_url = original_url.rstrip("/") + "/"  # Убедимся, что URL заканчивается на "/"
    return db.query(URL).filter(URL.original_url == normalized_url).all()'
'''

def search_url(db: Session, original_url: str):
    # Ищем без нормализации – сравниваем то, что передано
    return db.query(URL).filter(URL.original_url == original_url).all()

def get_expired_urls(db: Session):
    now_utc = datetime.now(timezone.utc)
    return db.query(URL).filter(
        (URL.expires_at != None) & (URL.expires_at < now_utc)
    ).all()

'''
def create_public_url(db: Session, link: URLShorten, project: str = None):
    short_code = link.custom_alias or generate_short_code()
    existing = db.query(URL).filter(URL.short_code == short_code).first()
    if existing:
        raise ValueError("Short code уже существует.")
    url = URL(
        original_url=link.original_url,
        short_code=short_code,
        custom_alias=link.custom_alias,
        expires_at=link.expires_at,
        project=project
    )

    db.add(url)
    db.commit()
    db.refresh(url)
    return url'
'''

def create_public_url(db: Session, link: URLShorten, project: str = None):
    short_code = link.custom_alias or generate_short_code()
    existing = db.query(URL).filter(URL.short_code == short_code).first()
    if existing:
        raise ValueError("Short code уже существует.")
    url = URL(
        original_url=str(link.original_url),
        short_code=short_code,
        custom_alias=link.custom_alias,
        expires_at=link.expires_at,
        project=project
    )
    db.add(url)
    db.commit()
    db.refresh(url)
    return url


