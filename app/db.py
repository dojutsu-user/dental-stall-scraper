import json
import os

from typing import List
from abc import ABC, abstractmethod
from typing import List

from app.logger import logger
from app.models import Product


class BaseProductStorage(ABC):
    @abstractmethod
    def load_existing_products(self) -> List[Product]:
        """Load existing products from storage"""
        pass

    @abstractmethod
    def save_products(self, products: List[Product]):
        """Save products to storage"""
        pass


class ProductStorage(BaseProductStorage):
    def __init__(self, file_path: str):
        self.file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    def load_existing_products(self) -> List[Product]:
        """Load existing products from a JSON file"""
        if not os.path.isfile(self.file_path):
            return []

        with open(self.file_path, "r") as f:
            if f.readable() and os.stat(self.file_path).st_size == 0:
                return []

            f.seek(0)
            return [Product(**data) for data in json.load(f)]

    def save_products(self, products: List[Product]):
        """Save products to a local JSON file"""
        existing_products = self.load_existing_products()

        existing_products_map = {
            p.product_id: i for i, p in enumerate(existing_products)}
        updated_products = existing_products[:]

        new = 0
        updated = 0

        for product in products:
            if product.product_id not in existing_products_map:
                updated_products.append(product)
                new += 1
            else:
                index = existing_products_map[product.product_id]
                updated_products[index] = product
                updated += 1

        with open(self.file_path, "w") as f:
            json.dump([p.model_dump() for p in updated_products], f, indent=4)

        return [new, updated]
