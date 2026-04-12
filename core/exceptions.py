"""
Custom exception classes for the sentiment analysis chatbot application
"""


class ChatbotException(Exception):
    """Base exception for all chatbot-related errors"""
    pass


class ScraperException(ChatbotException):
    """Exception raised during web scraping operations"""
    pass


class ScraperNetworkException(ScraperException):
    """Exception raised for network-related scraping errors"""
    pass


class ScraperParsingException(ScraperException):
    """Exception raised for HTML parsing errors"""
    pass


class ChatbotLLMException(ChatbotException):
    """Exception raised for LLM API errors"""
    pass


class ConfigurationException(ChatbotException):
    """Exception raised for configuration errors"""
    pass


class APIKeyException(ConfigurationException):
    """Exception raised when API key is missing or invalid"""
    pass


class ValidationException(ChatbotException):
    """Exception raised for data validation errors"""
    pass


class ResponseGenerationException(ChatbotException):
    """Exception raised when response generation fails"""
    pass
