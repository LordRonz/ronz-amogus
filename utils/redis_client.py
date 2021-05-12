import aredis
import os

class RedisClient(object):
    def __init__(self):
        self.r = aredis.StrictRedis(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),
            password=os.getenv('REDIS_PASS'),
        )

redis_client = RedisClient()
