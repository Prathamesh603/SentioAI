"""
Product information web scraper with logging and error handling
Supports multiple selector strategies for different website structures
"""

import requests
from bs4 import BeautifulSoup
import re
import json
from typing import Optional, Dict, Any
from core.logger import get_logger
from core.exceptions import (
    ScraperException,
    ScraperNetworkException,
    ScraperParsingException
)

logger = get_logger("applog")

# HTTP Headers for web requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive"
}


def get_soup(url: str) -> Optional[BeautifulSoup]:
    """
    Fetch and parse webpage with error handling
    
    Args:
        url: URL to scrape
    
    Returns:
        BeautifulSoup object or None if request fails
    
    Raises:
        ScraperNetworkException: If network request fails
    """
    try:
        logger.info(f"Fetching URL: {url}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        soup = BeautifulSoup(response.text, "html.parser")
        logger.info(f"Successfully fetched: {url}")
        return soup
    except requests.exceptions.Timeout:
        error_msg = f"Request timeout for {url}"
        logger.error(error_msg)
        raise ScraperNetworkException(error_msg)
    except requests.exceptions.ConnectionError as e:
        error_msg = f"Connection error for {url}: {str(e)}"
        logger.error(error_msg)
        raise ScraperNetworkException(error_msg)
    except requests.exceptions.RequestException as e:
        error_msg = f"Error fetching {url}: {str(e)}"
        logger.error(error_msg)
        raise ScraperNetworkException(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error fetching {url}: {str(e)}"
        logger.error(error_msg)
        raise ScraperException(error_msg)


def get_product_info(url: str) -> str:
    """
    Extract product information with multiple selector fallbacks
    
    Args:
        url: Product page URL
    
    Returns:
        Product information text or empty string if not found
    """
    try:
        logger.debug(f"Extracting product info from {url}")
        soup = get_soup(url)
        
        if soup is None:
            logger.warning(f"Could not parse content from {url}")
            return ""
        
        # Try multiple selectors for different website structures
        selectors = [
            ("div", "centerColAlign"),      # Amazon
            ("div", "a-section"),           # Amazon alternative
            ("div", "product-info"),        # Generic
            ("main", None),                 # Main content
        ]
        
        for tag, class_name in selectors:
            try:
                if class_name:
                    element = soup.find(tag, class_=class_name)
                else:
                    element = soup.find(tag)
                
                if element:
                    text = element.get_text(" ", strip=True)
                    if len(text) > 50:  # Only return if substantial content
                        logger.info(f"Found product info using {tag}.{class_name}")
                        return text
            except Exception as e:
                logger.debug(f"Error trying selector {tag}.{class_name}: {str(e)}")
                continue
        
        # Fallback: get all body text
        try:
            body = soup.find("body")
            if body:
                text = body.get_text(" ", strip=True)[:2000]
                logger.info("Using fallback body text for product info")
                return text
        except Exception as e:
            logger.debug(f"Error extracting body text: {str(e)}")
        
        logger.warning(f"No product info found for {url}")
        return ""
    
    except ScraperNetworkException:
        raise
    except Exception as e:
        error_msg = f"Error extracting product info from {url}: {str(e)}"
        logger.error(error_msg)
        raise ScraperParsingException(error_msg)


def get_reviews(url: str) -> str:
    """
    Extract reviews with multiple selector fallbacks
    
    Args:
        url: Product page URL
    
    Returns:
        Reviews text or empty string if not found
    """
    try:
        logger.debug(f"Extracting reviews from {url}")
        soup = get_soup(url)
        
        if soup is None:
            logger.warning(f"Could not parse content from {url} for reviews")
            return ""
        
        # Try multiple selectors for different website structures
        selectors = [
            ("div", "Top reviews"),                                     # Generic
            ("div", "cm_cr_grid_center_right_non_images_widgets"),  # Amazon reviews
            ("div", "a-section review"),                            # Amazon alternative
            ("section", "reviews"),                                 # Generic alternative
        ]
        
        for tag, class_name in selectors:
            try:
                element = soup.find(tag, class_=class_name)
                if element:
                    text = element.get_text(" ", strip=True)
                    if len(text) > 20:  # Only return if substantial content
                        logger.info(f"Found reviews using {tag}.{class_name}")
                        return text
            except Exception as e:
                logger.debug(f"Error trying selector {tag}.{class_name}: {str(e)}")
                continue
        
        # Fallback: look for any element with "review" in class or id
        try:
            review_elements = soup.find_all(class_=lambda x: x and "review" in x.lower())
            if review_elements:
                text = " ".join([elem.get_text(" ", strip=True) for elem in review_elements[:5]])[:2000]
                logger.info("Using fallback review elements")
                return text
        except Exception as e:
            logger.debug(f"Error extracting review elements: {str(e)}")
        
        logger.warning(f"No reviews found for {url}")
        return ""
    
    except ScraperNetworkException:
        raise
    except Exception as e:
        error_msg = f"Error extracting reviews from {url}: {str(e)}"
        logger.error(error_msg)
        raise ScraperParsingException(error_msg)


def get_rating(url: str) -> Optional[float]:
    """
    Extract rating from product page with multiple fallback strategies
    
    Args:
        url: Product page URL
    
    Returns:
        Rating value (0-5) or None if not found
    """
    try:
        logger.debug(f"Extracting rating from {url}")
        soup = get_soup(url)
        
        if soup is None:
            logger.warning(f"Could not parse content from {url} for rating")
            return None
        
        # Strategy 1: Look for Amazon rating badge/card
        logger.debug("Strategy 1: Looking for rating in HTML elements")
        rating_selectors = [
            ("span", lambda x: x and "a-size-small" in x and "a-color-base" in x),  # Amazon rating display
            ("span", lambda x: x and "a-icon-star" in x),           # Amazon star class
            ("div", lambda x: x and "rating" in x.lower()),         # Any rating class
            ("span", lambda x: x and "star" in x.lower()),          # Any star class
            ("div", lambda x: x and "a-star" in x),                 # Amazon star div
        ]
        
        for tag, class_filter in rating_selectors:
            try:
                elements = soup.find_all(tag, class_=class_filter)
                for element in elements:
                    text = element.get_text(strip=True)
                    # Try to extract number (e.g., "4.5 out of 5 stars", "4.5", "4.5/5")
                    match = re.search(r'(\d+[.,]\d+|\d+)\s*(?:out of|\/|\sstars)?', text)
                    if match:
                        try:
                            rating_str = match.group(1).replace(',', '.')
                            rating = float(rating_str)
                            if 0 <= rating <= 5:
                                logger.info(f"Found rating: {rating} from {tag} element")
                                return rating
                        except ValueError as e:
                            logger.debug(f"Could not convert rating string: {str(e)}")
                            continue
            except Exception as e:
                logger.debug(f"Error trying rating selector: {str(e)}")
                continue
        
        # Strategy 2: Search for rating in common patterns
        logger.debug("Strategy 2: Looking for rating in text patterns")
        text_content = soup.get_text()
        
        # Pattern 1: "4.5 out of 5" or "4.5/5"
        pattern1 = r'(\d+[.,]\d+)\s*(?:out of|\/)\s*5'
        match1 = re.search(pattern1, text_content)
        if match1:
            try:
                rating = float(match1.group(1).replace(',', '.'))
                if 0 <= rating <= 5:
                    logger.info(f"Found rating (pattern: X out of 5): {rating}")
                    return rating
            except ValueError as e:
                logger.debug(f"Could not convert rating from pattern 1: {str(e)}")
        
        # Pattern 2: "Rated 4.5 stars"
        pattern2 = r'[Rr]ated\s+(\d+[.,]\d+)\s+stars'
        match2 = re.search(pattern2, text_content)
        if match2:
            try:
                rating = float(match2.group(1).replace(',', '.'))
                if 0 <= rating <= 5:
                    logger.info(f"Found rating (pattern: Rated X stars): {rating}")
                    return rating
            except ValueError as e:
                logger.debug(f"Could not convert rating from pattern 2: {str(e)}")
        
        # Pattern 3: Just "4.5 ★" or "4.5★"
        pattern3 = r'(\d+[.,]\d+)\s*[★⭐]'
        match3 = re.search(pattern3, text_content)
        if match3:
            try:
                rating = float(match3.group(1).replace(',', '.'))
                if 0 <= rating <= 5:
                    logger.info(f"Found rating (pattern: X ★): {rating}")
                    return rating
            except ValueError as e:
                logger.debug(f"Could not convert rating from pattern 3: {str(e)}")
        
        # Strategy 3: Look in meta tags (if website uses structured data)
        logger.debug("Strategy 3: Looking for rating in meta tags")
        meta_rating = soup.find("meta", {"itemprop": "ratingValue"})
        if meta_rating and meta_rating.get("content"):
            try:
                rating = float(meta_rating.get("content"))
                if 0 <= rating <= 5:
                    logger.info(f"Found rating in meta tag: {rating}")
                    return rating
            except ValueError as e:
                logger.debug(f"Could not convert meta tag rating: {str(e)}")
        
        # Strategy 4: Look for rating in JSON-LD structured data
        logger.debug("Strategy 4: Looking for rating in JSON-LD structured data")
        scripts = soup.find_all("script", {"type": "application/ld+json"})
        for script in scripts:
            try:
                if script.string:
                    data = json.loads(script.string)
                    if isinstance(data, dict) and "aggregateRating" in data:
                        rating = float(data["aggregateRating"].get("ratingValue", 0))
                        if 0 <= rating <= 5:
                            logger.info(f"Found rating in JSON-LD: {rating}")
                            return rating
            except (json.JSONDecodeError, ValueError, TypeError, AttributeError) as e:
                logger.debug(f"Error parsing JSON-LD: {str(e)}")
                continue
        
        logger.warning(f"Could not extract rating from {url}")
        return None
    
    except ScraperNetworkException:
        raise
    except Exception as e:
        error_msg = f"Error extracting rating from {url}: {str(e)}"
        logger.error(error_msg)
        raise ScraperParsingException(error_msg)
