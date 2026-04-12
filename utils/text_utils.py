"""
Text processing utilities
Provides text cleaning, normalization, and analysis functions
"""

import re
from typing import List
from core.logger import get_logger

logger = get_logger("applog")


def clean_text(text: str) -> str:
    """
    Clean and normalize text
    Removes extra whitespace and special characters
    
    Args:
        text: Text to clean
    
    Returns:
        Cleaned text
    """
    try:
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\!\?\,\-]', '', text)
        logger.debug("Text cleaned successfully")
        return text.strip()
    except Exception as e:
        logger.error(f"Error cleaning text: {str(e)}")
        return text


def extract_keywords(text: str, num_keywords: int = 5) -> List[str]:
    """
    Extract important keywords from text
    Filters out common stop words and normalizes results
    
    Args:
        text: Text to extract keywords from
        num_keywords: Number of keywords to extract
    
    Returns:
        List of extracted keywords
    """
    try:
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'
        }
        
        # Split and filter
        words = text.lower().split()
        keywords = [
            word.strip('.,!?;:') 
            for word in words 
            if word.lower() not in stop_words and len(word) > 3
        ]
        
        # Get unique keywords
        unique_keywords = []
        seen = set()
        for keyword in keywords:
            if keyword not in seen:
                unique_keywords.append(keyword)
                seen.add(keyword)
        
        result = unique_keywords[:num_keywords]
        logger.debug(f"Extracted {len(result)} keywords from text")
        return result
    
    except Exception as e:
        logger.error(f"Error extracting keywords: {str(e)}")
        return []


def calculate_readability_score(text: str) -> float:
    """
    Calculate text readability score (0-100)
    Based on sentence length and word complexity
    
    Args:
        text: Text to analyze
    
    Returns:
        Readability score (0-100)
    """
    try:
        sentences = text.split('. ')
        if not sentences or not sentences[0]:
            return 0.0
        
        words = text.split()
        
        if not words:
            return 0.0
        
        avg_sentence_length = len(words) / len(sentences)
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Flesch Reading Ease approximation
        # Ideal: 8-10 words per sentence, 4-5 characters per word
        score = 100.0
        
        # Penalize for long sentences
        if avg_sentence_length > 15:
            score -= (avg_sentence_length - 15) * 2
        elif avg_sentence_length < 5:
            score -= (5 - avg_sentence_length) * 1.5
        
        # Penalize for long words
        if avg_word_length > 6:
            score -= (avg_word_length - 6) * 1.5
        elif avg_word_length < 3:
            score -= (3 - avg_word_length) * 1.0
        
        # Ensure score is within bounds
        score = max(0.0, min(100.0, score))
        logger.debug(f"Readability score calculated: {score:.2f}")
        return score
    
    except Exception as e:
        logger.error(f"Error calculating readability score: {str(e)}")
        return 0.0
