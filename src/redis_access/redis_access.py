
import redis

from constants import REDIS_ADDR, REDIS_PORT


r = redis.Redis(host=REDIS_ADDR, port=REDIS_PORT, decode_responses=True)

def set_to_redis(key: str, value):
    r.set(key, value)

def get_from_redis(key: str):
    return r.get(key)