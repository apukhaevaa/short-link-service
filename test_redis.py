from database import redis_client

redis_client.set("test_key_ssl", "test_value_ssl")
value = redis_client.get("test_key_ssl")

print("Полученное значение из Redis через SSL:", value)