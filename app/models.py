from pydantic import BaseModel


class Product(BaseModel):
    product_id: str
    product_title: str
    product_price: float
    path_to_image: str


class ScrapeRequest(BaseModel):
    total_pages: int
