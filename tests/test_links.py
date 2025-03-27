# tests/test_links.py
import pytest
from fastapi.testclient import TestClient
from main import app
from datetime import datetime, timedelta

client = TestClient(app)

@pytest.fixture
def auth_header():
    # Регистрируем пользователя и получаем токен
    # пользователь уже зарегистрирован.
    response = client.post("/auth/token", data={"username": "admin", "password": "123456"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_short_link(auth_header):
    data = {
        "original_url": "https://google.com",
        "custom_alias": "testlink",
        "expires_at": (datetime.utcnow() + timedelta(days=1)).isoformat()
    }
    response = client.post("/links/shorten", json=data, headers=auth_header)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["short_code"] == "testlink"
    assert json_data["original_url"] == "https://google.com"

def test_redirect_link(auth_header):
    # Сначала создаём ссылку
    data = {"original_url": "https://example.com", "custom_alias": "redirecttest", "expires_at": None}
    create_resp = client.post("/links/shorten", json=data, headers=auth_header)
    assert create_resp.status_code == 200
    # Выполняем редирект с Accept: application/json для получения JSON-ответа
    response = client.get("/links/redirecttest", headers={"Accept": "application/json"})
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["original_url"] == "https://example.com"

def test_update_link(auth_header):
    # Создаём ссылку для обновления
    data = {"original_url": "https://oldsite.com", "custom_alias": "updatetest", "expires_at": None}
    create_resp = client.post("/links/shorten", json=data, headers=auth_header)
    assert create_resp.status_code == 200
    # Обновляем ссылку
    update_data = {"original_url": "https://newsite.com"}
    update_resp = client.put("/links/updatetest", json=update_data, headers=auth_header)
    assert update_resp.status_code == 200
    assert update_resp.json()["original_url"] == "https://newsite.com"

def test_delete_link(auth_header):
    # Создаём ссылку для удаления
    data = {"original_url": "https://deletetest.com", "custom_alias": "deletetest", "expires_at": None}
    create_resp = client.post("/links/shorten", json=data, headers=auth_header)
    assert create_resp.status_code == 200
    # Удаляем ссылку
    delete_resp = client.delete("/links/deletetest", headers=auth_header)
    assert delete_resp.status_code == 200
    # Проверяем, что ссылка удалена (редирект должен вернуть 404)
    get_resp = client.get("/links/deletetest", headers={"Accept": "application/json"})
    assert get_resp.status_code == 404

def test_search_links(auth_header):
    # Создаём ссылку для поиска
    data = {"original_url": "https://searchtest.com", "custom_alias": "searchtest", "expires_at": None}
    client.post("/links/shorten", json=data, headers=auth_header)
    # Поиск ссылки по оригинальному URL
    search_resp = client.get("/links/search/?original_url=https://searchtest.com")
    assert search_resp.status_code == 200
    results = search_resp.json()
    # Проверяем, что найден хотя бы один результат
    assert isinstance(results, list)
    assert any(item["short_code"] == "searchtest" for item in results)