import json
import redis

from app.settings import get_settings
from app.scraper import Product

PRODUCT_CACHE_EXPIRATION_IN_SECONDS = 3600


class Cache:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host=get_settings(
        ).redis_host, port=get_settings().redis_port, db=get_settings().redis_db)

    def cache_product(self, product: Product):
        """Cache a product in Redis"""
        self.redis_client.setex(self.__get_product_cache_key(
            product), PRODUCT_CACHE_EXPIRATION_IN_SECONDS, json.dumps(product.model_dump()))

    def is_product_cached(self, product: Product) -> bool:
        """Check if product is already cached and hasn't changed"""
        cached_product = self.redis_client.get(
            self.__get_product_cache_key(product))
        if cached_product:
            cached_product_data = json.loads(cached_product)
            return cached_product_data['product_price'] == product.product_price
        return False

    def __get_product_cache_key(self, product: Product) -> str:
        """Generates and returns the cache key for the product"""
        return f"atlys_scraper_product__{product.product_id}"
