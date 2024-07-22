import redis
import os
from dotenv import load_dotenv

def connect_to_cache():
    load_dotenv()

    REDIS_CONFIG = {
        'host': os.getenv('REDIS_HOST'),
        'port': os.getenv('REDIS_PORT'),
        'db': os.getenv('REDIS_DB')
    }
    try:
        r = redis.Redis(**REDIS_CONFIG)
    except redis.RedisError as e:
        print(f"Error connecting to Redis: {e}")
    
    return r

def save_to_cache(r, products):
    try:
        for product in products:
            r.hmset(f"product:{product['product_title']}", product)
    except redis.RedisError as e:
        print(f"Error saving to Redis: {e}")


def read_from_cache(r, product_title):
    product_data = r.hgetall(f"product:{product_title}")
    if product_data:
        return {k.decode('utf-8'): v.decode('utf-8') for k, v in product_data.items()}
    return None

def update_cache(r, products):
    try:
        for product in products:
            r.hset(f"product:{product['product_title']}", "product_price", product['product_price'])

            print(f"Successfully updated price for product_id {product['product_title']} to {product['product_price']}")
    except redis.RedisError as e:
        print(f"Error updating Redis: {e}")