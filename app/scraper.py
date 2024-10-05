import os
import time
import base64
import requests

from app.models import Product
from app.logger import logger
from app.settings import get_settings
from app.cache import Cache

from typing import List
from uuid import uuid4
from bs4 import BeautifulSoup


class BaseScraper:
    def __init__(self, base_url: str, headers: dict = None, proxy: dict = None):
        self.base_url = base_url
        self.headers = headers or {}
        self.proxy = proxy

    def download_image(self, image_url: str, title: str) -> str:
        """Download and save the product image"""
        logger.info(f"Downloading image for product: {title}")
        parsed_title = self.__generate_image_filename(title)

        os.makedirs(get_settings().images_folder, exist_ok=True)

        image_response = requests.get(image_url)
        file_name = f"images/{parsed_title}.jpg".replace(" ", "_")

        with open(file_name, "wb") as f:
            f.write(image_response.content)

        return file_name

    def __generate_image_filename(self, product_title: str) -> str:
        """Generates and returns a unique file name"""
        unique_id = uuid4()
        safe_title = "".join(x for x in product_title if x.isalnum()
                             or x == "-").rstrip()
        return f"{safe_title}_{unique_id}"

    def scrape_page(self, page_number: int) -> List[Product]:
        """Scrape a single page of the product catalog"""
        raise NotImplementedError("Subclasses should implement this method.")

    def scrape(self) -> List[Product]:
        """Scrape products from all the pages"""
        raise NotImplementedError("Subclasses should implement this method.")


class DentalStallScraper(BaseScraper):
    def __init__(self):
        base_url = get_settings().dentalstall_base_url
        proxy = {"http": get_settings().proxy} if get_settings().proxy else None
        super().__init__(base_url=base_url, proxy=proxy)

        self.max_page_limit = get_settings().max_page_limit
        self.cache = Cache()
        self.max_retries = get_settings().dentalstall_max_retries

    def __scrape_page(self, page_number: int) -> List[Product]:
        """Scrape a single page of the product catalog"""
        logger.info(f"Scraping page {page_number}")
        attempt = 0

        while attempt < self.max_retries:
            try:
                url = self.base_url
                if page_number > 1:
                    url = f"{self.base_url}/page/{page_number}"
                response = requests.get(
                    url, headers=self.headers, proxies=self.proxy)
                response.raise_for_status()
                break
            except requests.RequestException as e:
                attempt = attempt + 1
                sleep_time = (attempt * self.max_retries) + 3
                logger.error(f"""Error fetching page {page_number}: {
                             e}. Retrying in {sleep_time} seconds...""")
                time.sleep(sleep_time)

                if attempt == self.max_retries:
                    logger.warning(f"""Failed to fetch page {page_number} after {
                        self.max_retries} attempts. Skipping this page.""")
                    return []

        soup = BeautifulSoup(response.text, 'html.parser')
        products = []

        for item in soup.find_all('div', class_='product-inner'):
            title = item.find(
                'h2', class_='woo-loop-product__title').text.strip()
            product_id = item.find(
                'div', class_='addtocart-buynow-btn').find('a')['data-product_id']

            price_element = item.find('span', class_='price')
            if price_element:
                discounted_price = price_element.find('ins')
                # if discounted price is present, use that price.
                if discounted_price:
                    price = float(
                        discounted_price.text.replace('₹', '').strip())
                else:
                    price = float(price_element.find(
                        'span', class_='amount').text.replace('₹', '').strip())
            else:
                logger.warning(f"No price found for product: {title}")
                continue

            if self.cache.is_product_cached(Product(
                    product_id=product_id,
                    product_title=title,
                    product_price=price,
                    path_to_image="")):
                continue

            image_url = item.find('img').get('data-lazy-src', '')
            if not image_url:
                logger.info(f"Image not found for product: {title} - {price}")
                continue

            image_path = self.download_image(image_url, title)
            product = Product(product_id=product_id, product_title=title,
                              product_price=price, path_to_image=image_path)
            products.append(product)

            logger.info(f"Scraped product: {title} - {price}")

        return products

    def scrape(self, total_pages: int) -> List[Product]:
        """Scrape products from all the pages"""
        logger.info(f"""Starting scraping process. Max Page limit: {
                    self.max_page_limit}, Total pages: {total_pages}""")

        pages = min(self.max_page_limit, total_pages)

        all_products = []
        for page in range(1, pages + 1):
            products = self.__scrape_page(page)
            all_products.extend(products)
        logger.info(f"""Scraping complete. Total products scraped: {
                    len(all_products)} from {pages} pages.""")

        return all_products
