# tests/test_crud.py
import pytest
from datetime import datetime, timedelta, timezone
from models import URL
from schemas import URLShorten
import crud

class FakeSession:
    def __init__(self):
        self.data = []
    def add(self, obj):
        self.data.append(obj)
    def commit(self):
        pass
    def refresh(self, obj):
        pass
    def query(self, model):
        return FakeQuery(self.data)
    def delete(self, obj):
        self.data.remove(obj)

class FakeQuery:
    def __init__(self, data):
        self.data = data
    def filter(self, *criteria):
        # очень упрощенная фильтрация, только для теста
        results = []
        for obj in self.data:
            match = True
            for crit in criteria:
                # crit может быть лямбда-функцией для проверки
                if callable(crit):
                    if not crit(obj):
                        match = False
                else:
                    # в реальном тесте нужно реализовать парсинг SQLAlchemy-выражений
                    match = False
            if match:
                results.append(obj)
        return FakeQuery(results)
    def first(self):
        return self.data[0] if self.data else None
    def all(self):
        return self.data

def test_update_url():
    session = FakeSession()
    # Создаем тестовую ссылку
    test_url = URL(
        original_url="https://old.com",
        short_code="testcode",
        custom_alias=None,
        expires_at=None,
        user_id=1,
        clicks=0,
        created_at=datetime.now(timezone.utc),
        last_used=None,
        project=None,
        expired=False
    )
    session.add(test_url)
    updated = crud.update_url(session, "testcode", "https://new.com")
    assert updated is not None
    assert updated.original_url == "https://new.com"

def test_delete_url():
    session = FakeSession()
    # Создаем тестовую ссылку
    test_url = URL(
        original_url="https://delete.com",
        short_code="deletecode",
        custom_alias=None,
        expires_at=None,
        user_id=1,
        clicks=0,
        created_at=datetime.now(timezone.utc),
        last_used=None,
        project=None,
        expired=False
    )
    session.add(test_url)
    deleted = crud.delete_url(session, "deletecode", 1)
    assert deleted is not None
    # После удаления ссылка должна отсутствовать
    assert session.query(URL).filter(lambda o: o.short_code == "deletecode") .first() is None