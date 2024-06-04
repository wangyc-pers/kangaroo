class RedisCache:
    def __init__(self, redis_url: str, prefix: str = "siteby_cache:"):
        try:
            self.redis = redis.from_url(redis_url)
            self.aioredis = aioredis.from_url(redis_url)
            self.prefix = prefix
        except redis.ConnectionError:
            raise ValueError(f"Failed to connect to Redis server at {redis_url}")

    def _pickle_loads(self, pickled_value):
        try:
            return pickle.loads(pickled_value)
        except pickle.UnpicklingError:
            raise ValueError("Failed to unpickle value")

    def _pickle_dumps(self, value):
        try:
            return pickle.dumps(value)
        except pickle.PicklingError:
            raise ValueError("Failed to pickle value")

    def get(self, key: str) -> Optional[Any]:
        pickled_value = self.redis.get(self.prefix + key)
        if pickled_value is None:
            return None
        return self._pickle_loads(pickled_value)

    def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        pickled_value = self._pickle_dumps(value)
        self.redis.set(self.prefix + key, pickled_value, ex=expire)

    def delete(self, key: str) -> None:
        self.redis.delete(self.prefix + key)

    async def async_get(self, key: str) -> Optional[Any]:
        pickled_value = await self.aioredis.get(self.prefix + key)
        if pickled_value is None:
            return None
        return self._pickle_loads(pickled_value)

    async def async_set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        pickled_value = self._pickle_dumps(value)
        await self.aioredis.set(self.prefix + key, pickled_value, ex=expire)

    async def async_delete(self, key: str) -> None:
        await self.aioredis.delete(self.prefix + key)