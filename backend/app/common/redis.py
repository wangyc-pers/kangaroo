import redis
from app.config import settings

redis_pool: redis.ConnectionPool = None


def init_redis_pool(redis_url: str):
    global redis_pool
    redis_pool = redis.ConnectionPool.from_url(redis_url)


def get_redis():
    if redis_pool is None:
        assert settings.REDIS_URL, "Redis URL is not set"
        init_redis_pool(str(settings.REDIS_URL))()
    return redis.Redis(connection_pool=redis_pool)
