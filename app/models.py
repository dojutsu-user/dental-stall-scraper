from pydantic import BaseModel, Field, field_validator


class Product(BaseModel):
    product_id: str
    product_title: str
    product_price: float
    path_to_image: str


class ScrapeRequest(BaseModel):
    total_pages: int = Field(...,
                             description="Total number of pages to scrape")

    @field_validator('total_pages')
    @classmethod
    def total_pages_must_be_positive(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("total_pages must be greater than 0")
        return value
