import redis
import os

def get_redis_connection(): 
    r = redis.Redis(
        host= os.getenv('REDIS_HOST', '127.0.0.1'),
        port= os.getenv('REDIS_PORT', 6379), 
        password=os.getenv('REDIS_PWD', '123456'),
        decode_responses=True)
    return r

def add_to_cache(long_url, short_id):
    """Add the mapping of long url and short id to the cache"""
    r = get_redis_connection()
    r.set(long_url,short_id)
    r.set(short_id,long_url)

def get_from_cache(key):
    """Get the mapped value with a given key from the cache"""
    r = get_redis_connection()
    return r.get(key)

def delete_from_cache(key):
    """Delete the value with a given key"""
    r = get_redis_connection()
    r.delete(key)