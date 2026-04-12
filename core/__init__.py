"""Core module for logging and exception handling"""

from .logger import setup_logger, get_logger
from .exceptions import (
    ChatbotException,
    ScraperException,
    ScraperNetworkException,
    ScraperParsingException,
    ChatbotLLMException,
    ConfigurationException,
    APIKeyException,
    ValidationException,
    ResponseGenerationException
)

__all__ = [
    "setup_logger",
    "get_logger",
    "ChatbotException",
    "ScraperException",
    "ScraperNetworkException",
    "ScraperParsingException",
    "ChatbotLLMException",
    "ConfigurationException",
    "APIKeyException",
    "ValidationException",
    "ResponseGenerationException"
]
