import redis
import json
from datetime import datetime

class Cache:
    """Redis cache handler Class"""
    redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

    def set_cache(self, key: str, value: dict) -> bool:
        """
        Set value in cache with expiration.

        param key: Redis key
        param value: Value to set in Redis
        return: Success status
        """
        # Serialize Python object to JSON string
        self.redis_client.set(key, json.dumps(value, default=self._datetime_encoder), ex=300)
        return True

    def get_cache(self, key: str) -> list:
        """
        Retrieve value from cache.

        param key: Redis key
        return: Cached value or None if no value
        """
        cached_value = self.redis_client.get(key)
        if cached_value:
            # Deserialize JSON string back to Python object
            return json.loads(cached_value, object_hook=self._datetime_decoder)
        return None

    def delete_cache(self, key: str) -> bool:
        """
        Delete key from cache.

        param key: Redis key
        return: Success status
        """
        self.redis_client.delete(key)
        return True

    @staticmethod
    def _datetime_encoder(obj):
        """Custom JSON encoder for datetime objects."""
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO 8601 string
        raise TypeError("Type not serializable")

    @staticmethod
    def _datetime_decoder(obj):
        """Custom JSON decoder for datetime objects."""
        for key, value in obj.items():
            try:
                obj[key] = datetime.fromisoformat(value)  # Parse ISO 8601 string to datetime
            except (ValueError, TypeError):
                pass
        return obj
