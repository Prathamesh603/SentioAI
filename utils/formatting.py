"""
Response formatting and display utilities
Provides formatting functions for output and UI components
"""

import re
from core.logger import get_logger

logger = get_logger("applog")


def format_response(response_text: str, max_length: int = None) -> str:
    """
    Format bot response with proper markdown
    
    Args:
        response_text: Raw response text
        max_length: Maximum length to keep (truncates if exceeded)
    
    Returns:
        Formatted response text
    """
    try:
        if max_length and len(response_text) > max_length:
            response_text = response_text[:max_length] + "..."
        
        # Add line breaks for better readability
        response_text = re.sub(r'\n\n+', '\n\n', response_text)
        
        logger.debug(f"Response formatted (length: {len(response_text)})")
        return response_text
    
    except Exception as e:
        logger.error(f"Error formatting response: {str(e)}")
        return response_text


def get_sentiment_color(sentiment: str) -> str:
    """
    Get color code for sentiment visualization
    
    Args:
        sentiment: Sentiment type ('positive', 'negative', 'neutral')
    
    Returns:
        Hex color code
    """
    color_map = {
        "positive": "#4CAF50",      # Green
        "negative": "#f44336",      # Red
        "neutral": "#FFC107"        # Yellow/Orange
    }
    color = color_map.get(sentiment, "#9E9E9E")  # Gray default
    logger.debug(f"Color for sentiment '{sentiment}': {color}")
    return color


def get_sentiment_emoji(sentiment: str) -> str:
    """
    Get emoji representation for sentiment
    
    Args:
        sentiment: Sentiment type ('positive', 'negative', 'neutral')
    
    Returns:
        Emoji character
    """
    emoji_map = {
        "positive": "😊",
        "negative": "😞",
        "neutral": "😐"
    }
    emoji = emoji_map.get(sentiment, "🤔")
    logger.debug(f"Emoji for sentiment '{sentiment}': {emoji}")
    return emoji
