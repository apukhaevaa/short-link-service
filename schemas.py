from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True

class URLBase(BaseModel):
    original_url: HttpUrl

class URLShorten(URLBase):
    custom_alias: Optional[str] = None
    expires_at: Optional[datetime] = None

class URLInfo(URLBase):
    short_code: str
    clicks: int
    created_at: datetime
    last_used: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    project: Optional[str] = None
    expired: Optional[bool] = False
    class Config:
        orm_mode = True