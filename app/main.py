import os

from app.settings import get_settings
from app.scraper import DentalStallScraper
from app.db import ProductStorage
from app.cache import Cache
from app.notification import LoggingNotification
from app.logger import logger
from app.models import ScrapeRequest

from fastapi import FastAPI, Depends, HTTPException, Header

app = FastAPI()


def authenticate(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        logger.error(
            "Missing or invalid token format in Authorization header.")
        raise HTTPException(
            status_code=401, detail="Unauthorized: Invalid token format")

    token = authorization[len("Bearer "):]

    if token != get_settings().static_token:
        logger.error("Unauthorized access attempt with token: %s", token)
        raise HTTPException(
            status_code=401, detail="Unauthorized: Invalid token")

    return token


@app.post("/scrape")
def scrape(request: ScrapeRequest, token: str = Depends(authenticate)):
    logger.info("Scraping initiated via API")
    scraper = DentalStallScraper()
    cache = Cache()
    notifier = LoggingNotification()
    db = ProductStorage(os.path.abspath(get_settings().output_json_filename))

    scraped_products = scraper.scrape(request.total_pages)
    new_count = 0
    updated_count = 0

    for product in scraped_products:
        if not cache.is_product_cached(product):
            new, updated = db.save_products([product])
            cache.cache_product(product)

            new_count += new
            updated_count += updated

    notifier.notify(new_count, updated_count)
    logger.info(f"""Scraping session completed. {
                new_count} new products saved and {updated_count} products updated.""")

    return {"success": True, "new": new_count, "updated": updated_count}
