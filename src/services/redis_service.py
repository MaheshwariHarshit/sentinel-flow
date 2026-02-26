import redis
import json
from src.core.config import config

class RedisCache:
    def __init__(self):
        self.client = redis.Redis.from_url(config.database.redis_uri, decode_responses=True)

    def set_cache(self, key: str, value: dict, expire_seconds: int = 3600):
        try:
            self.client.setex(key, expire_seconds, json.dumps(value))
        except redis.RedisError as e:
            print(f"Redis set error: {e}")

    def get_cache(self, key: str):
        try:
            val = self.client.get(key)
            if val:
                return json.loads(val)
        except redis.RedisError as e:
            print(f"Redis get error: {e}")
            return None

redis_cache = RedisCache()
