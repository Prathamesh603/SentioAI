"""
Sentiment Analysis Chatbot - Main Entry Point
Professional chatbot with LangChain integration and web scraping
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from core.logger import setup_logger, get_logger

# Initialize logging
setup_logger("sentiment_analysis_chatbot", log_level="INFO")
logger = get_logger(__name__)

__version__ = "1.0.0"
__author__ = "Your Name"

logger.info(f"Sentiment Analysis Chatbot v{__version__} initialized")

# Export main classes
from chatbot import ChatBot
from metrics import MetricsTracker
from scrapers import get_product_info, get_reviews, get_rating
from utils import (
    calculate_sentiment,
    format_response,
    extract_keywords,
    calculate_readability_score,
    get_sentiment_color,
    get_sentiment_emoji
)

__all__ = [
    "ChatBot",
    "MetricsTracker",
    "get_product_info",
    "get_reviews",
    "get_rating",
    "calculate_sentiment",
    "format_response",
    "extract_keywords",
    "calculate_readability_score",
    "get_sentiment_color",
    "get_sentiment_emoji",
    "__version__"
]
