"""Scrapers module for web scraping functionality"""

from .product_scraper import (
    get_soup,
    get_product_info,
    get_reviews,
    get_rating,
    HEADERS
)

__all__ = [
    "get_soup",
    "get_product_info",
    "get_reviews",
    "get_rating",
    "HEADERS"
]
