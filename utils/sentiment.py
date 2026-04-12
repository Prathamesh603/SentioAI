"""
Sentiment analysis utilities
Provides sentiment detection and confidence scoring
"""

from typing import Tuple
from core.logger import get_logger

logger = get_logger("applog")


def calculate_sentiment(text: str) -> Tuple[str, float]:
    """
    Simple sentiment analysis based on keyword matching
    
    Args:
        text: Text to analyze
    
    Returns:
        Tuple of (sentiment: str, confidence: float)
        sentiment: 'positive', 'negative', or 'neutral'
        confidence: 0.0 to 1.0
    """
    try:
        # Define sentiment keywords
        positive_keywords = [
            "good", "great", "excellent", "amazing", "wonderful", "fantastic",
            "love", "like", "happy", "grateful", "perfect", "best", "awesome",
            "thanks", "thank you", "please", "help", "appreciate"
        ]
        
        negative_keywords = [
            "bad", "terrible", "awful", "horrible", "hate", "dislike", "angry",
            "frustrated", "upset", "worst", "useless", "broken", "error",
            "fail", "failed", "problem", "issue", "bug"
        ]
        
        # Preprocess text
        text_lower = text.lower()
        
        # Count occurrences
        positive_count = sum(1 for word in positive_keywords if word in text_lower)
        negative_count = sum(1 for word in negative_keywords if word in text_lower)
        
        # Determine sentiment
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            logger.debug(f"No sentiment keywords found, returning neutral")
            return "neutral", 0.5
        
        positive_ratio = positive_count / total_sentiment_words
        
        # Determine sentiment and confidence
        if positive_ratio > 0.6:
            sentiment = "positive"
            confidence = min(positive_ratio, 0.95)
        elif positive_ratio < 0.4:
            sentiment = "negative"
            confidence = min(1 - positive_ratio, 0.95)
        else:
            sentiment = "neutral"
            confidence = 0.5
        
        logger.debug(f"Calculated sentiment: {sentiment} (confidence: {confidence:.2f})")
        return sentiment, confidence
    
    except Exception as e:
        logger.error(f"Error calculating sentiment: {str(e)}")
        return "neutral", 0.0
