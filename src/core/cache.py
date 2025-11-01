import json

from redis import asyncio as redis_async
from sqlalchemy import DateTime
import pickle


from src.core.settings import settings


cache = redis_async.Redis.from_url(settings.REDIS_URL)



async def set_cache(key: str, value):
    serialized_data = pickle.dumps(value)
    await cache.set(key, serialized_data)

async def get_cache(key: str):
    data_bytes = await cache.get(key)
    if not data_bytes:
        return None

    try:
        deserialized_data = pickle.loads(data_bytes)
        return deserialized_data
    except Exception as e:
        print(f"Ошибка десериализации: {e}")
        return None

