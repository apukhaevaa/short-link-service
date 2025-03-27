# locustfile.py
from locust import HttpUser, task, between
import json
from datetime import datetime, timedelta

class LinkShortenerUser(HttpUser):
    wait_time = between(1, 3)
    @task
    def create_link(self):
        url = "https://example.com"
        custom_alias = "load" + str(self.environment.runner.user_count)
        expires_at = (datetime.utcnow() + timedelta(days=1)).isoformat()
        payload = {
            "original_url": url,
            "custom_alias": custom_alias,
            "expires_at": expires_at
        }
        headers = {"Content-Type": "application/json"}
        self.client.post("/links/shorten", data=json.dumps(payload), headers=headers)

    @task
    def redirect_link(self):
        # Попытка редиректа по фиксированному short_code, можно сделать случайный или параметризованный
        self.client.get("/links/testredirect", name="redirect_link")