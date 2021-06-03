import aioredis
import os

class RedisClient:
    __slots__ = ('r')
    def __init__(self):
        address = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}"
        self.r = aioredis.from_url(address, password=os.getenv('REDIS_PASS'))

redis_client = RedisClient()
