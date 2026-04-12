"""
Core chatbot class with LangChain integration
Handles conversation management and response generation
"""

import os
import time
import re
from datetime import datetime
from typing import Dict, Any, List, Optional

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

from core.logger import get_logger
from core.exceptions import (
    ChatbotException,
    ChatbotLLMException,
    APIKeyException,
    ResponseGenerationException,
    ScraperException
)
from scrapers import get_product_info, get_reviews, get_rating
from utils import calculate_sentiment

# Get the shared logger instance
logger = get_logger("applog")

load_dotenv()


class ChatBot:
    """Professional Chatbot with Groq API Integration via LangChain"""
    
    def __init__(self):
        """Initialize chatbot with LLM and configuration"""
        try:
            logger.info("Initializing ChatBot...")
            
            # Load API key
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                error_msg = "GROQ_API_KEY not found in environment variables"
                logger.error(error_msg)
                raise APIKeyException(error_msg)
            
            logger.debug("API key loaded successfully")
            
            # Initialize LLM
            self.llm = ChatGroq(
                api_key=api_key,
                model="llama-3.3-70b-versatile",
                temperature=0.7
            )
            
            self.model = "llama-3.3-70b-versatile"
            self.temperature = 0.7
            self.conversation_history = []
            self.scraped_data = {}  # Store scraped data from URLs
            
            logger.info(f"LLM initialized with model: {self.model}")
            
            # System prompt
            self.system_prompt = """You are a professional, helpful AI assistant specialized in providing detailed product analysis.
        
WHEN SCRAPED DATA IS PROVIDED:
- Use the scraped product information, reviews, and ratings to answer questions
- Provide analysis based on REAL DATA from the provided content
- Reference specific details from the scraped data
- Give honest assessments based on actual reviews and product info

RESPONSE GUIDELINES:
1. Be concise yet comprehensive
2. Use clear formatting with bullet points and sections when appropriate
3. Provide actionable insights
4. Be professional and respectful
5. Always cite information from scraped data when available
6. End with a brief summary and recommendations

FORMAT:
- Start with a direct answer/summary
- Provide details in organized sections with real data
- End with key takeaways and recommendations

Keep responses focused and well-structured."""
            
            # Create prompt template
            self.prompt_template = PromptTemplate.from_template(
                self.system_prompt + "\n\nScraped Data:\n{scraped_context}\n\nConversation Context:\n{context}\n\nQuestion: {question}"
            )
            
            logger.info("ChatBot initialized successfully")
        
        except APIKeyException:
            raise
        except Exception as e:
            error_msg = f"Error initializing ChatBot: {str(e)}"
            logger.error(error_msg)
            raise ChatbotException(error_msg)
    
    def set_temperature(self, temp: float) -> None:
        """
        Set response temperature for creativity level
        
        Args:
            temp: Temperature value (0.0 to 1.0)
        """
        try:
            if not 0.0 <= temp <= 1.0:
                raise ValueError("Temperature must be between 0.0 and 1.0")
            
            self.temperature = temp
            self.llm.temperature = temp
            logger.info(f"Temperature set to {temp}")
        
        except Exception as e:
            error_msg = f"Error setting temperature: {str(e)}"
            logger.error(error_msg)
    
    def _extract_urls(self, text: str) -> List[str]:
        """
        Extract URLs from text
        
        Args:
            text: Text to extract URLs from
        
        Returns:
            List of extracted URLs
        """
        try:
            urls = re.findall(r'https?://[^\s]+', text)
            logger.debug(f"Extracted {len(urls)} URLs from text")
            return urls
        except Exception as e:
            logger.error(f"Error extracting URLs: {str(e)}")
            return []
    
    def _scrape_url(self, url: str) -> Dict[str, Any]:
        """
        Scrape data from URL using scraper functions
        
        Args:
            url: URL to scrape
        
        Returns:
            Dictionary with scraped data
        """
        try:
            logger.info(f"Starting scrape for: {url}")
            
            # Scrape data
            product_info = get_product_info(url)
            reviews = get_reviews(url)
            rating = get_rating(url)
            
            logger.debug(f"Product info length: {len(product_info)}")
            logger.debug(f"Reviews length: {len(reviews)}")
            logger.debug(f"Rating extracted: {rating}")
            
            if not product_info and not reviews:
                logger.warning(f"No data scraped from {url}")
            
            # Build scraped data dict
            scraped = {
                "url": url,
                "product_info": product_info[:2000] if product_info else "No product info found",
                "reviews": reviews[:2000] if reviews else "No reviews found",
                "rating": rating,
                "timestamp": datetime.now().isoformat(),
                "scraped": bool(product_info or reviews)
            }
            
            # Store in memory
            self.scraped_data[url] = scraped
            logger.info(f"Scraped data stored: {scraped.get('scraped')}")
            return scraped
        
        except ScraperException as e:
            logger.error(f"Scraper error for {url}: {str(e)}")
            error_data = {
                "url": url,
                "error": str(e),
                "product_info": f"Failed to scrape: {str(e)}",
                "reviews": "Unable to retrieve reviews",
                "rating": None,
                "scraped": False
            }
            self.scraped_data[url] = error_data
            return error_data
        
        except Exception as e:
            error_msg = f"Unexpected error scraping {url}: {str(e)}"
            logger.error(error_msg)
            error_data = {
                "url": url,
                "error": str(e),
                "product_info": f"Failed to scrape: {str(e)}",
                "reviews": "Unable to retrieve reviews",
                "rating": None,
                "scraped": False
            }
            self.scraped_data[url] = error_data
            return error_data
    
    def _get_scraped_context(self, user_input: str) -> str:
        """
        Get scraped data context for the current query
        
        Args:
            user_input: User's input text
        
        Returns:
            Formatted context string with scraped data
        """
        try:
            scraped_context = ""
            
            # Check if URLs exist in user input
            urls = self._extract_urls(user_input)
            
            # Scrape new URLs
            for url in urls:
                if url not in self.scraped_data:
                    self._scrape_url(url)
            
            # Add all scraped data to context
            if self.scraped_data:
                scraped_context = "AVAILABLE SCRAPED DATA:\n"
                for url, data in self.scraped_data.items():
                    scraped_context += f"\nURL: {url}\n"
                    if "error" not in data:
                        scraped_context += f"Product Info: {data.get('product_info', 'N/A')[:1000]}\n"
                        scraped_context += f"Reviews: {data.get('reviews', 'N/A')[:1000]}\n"
                    else:
                        scraped_context += f"Error: {data.get('error', 'Unknown error')}\n"
            else:
                scraped_context = "No scraped data available yet. Please provide a URL to scrape product information."
            
            return scraped_context
        
        except Exception as e:
            error_msg = f"Error getting scraped context: {str(e)}"
            logger.error(error_msg)
            return "Error retrieving scraped data."
    
    def generate_response(self, user_input: str) -> Dict[str, Any]:
        """
        Generate a structured response to user input
        
        Args:
            user_input: User's input text
        
        Returns:
            Dictionary with response content and metadata
        """
        start_time = time.time()
        
        try:
            logger.info(f"Generating response to: {user_input[:100]}...")
            
            # Get scraped data context
            scraped_context = self._get_scraped_context(user_input)
            
            # Build conversation context from history
            context = self._build_context()
            
            # Create the chain with LangChain
            chain = self.prompt_template | self.llm
            
            logger.debug("Invoking LLM chain...")
            
            # Invoke the chain with scraped data
            response = chain.invoke({
                "scraped_context": scraped_context,
                "context": context,
                "question": user_input
            })
            
            response_text = response.content
            
            logger.debug(f"Received response of length: {len(response_text)}")
            
            # Store in history
            self.conversation_history.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now()
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": response_text,
                "timestamp": datetime.now()
            })
            
            # Calculate metadata
            response_time = time.time() - start_time
            sentiment, confidence = calculate_sentiment(scraped_context)
            
            # Get scraped URLs from this query
            scraped_urls = self._extract_urls(user_input)
            
            # Get rating from scraped data if available
            scraped_rating = None
            for url in scraped_urls:
                if url in self.scraped_data and self.scraped_data[url].get("rating"):
                    scraped_rating = self.scraped_data[url]["rating"]
                    break
            
            metadata = {
                "sentiment": sentiment,
                "confidence": confidence,
                "length": len(response_text),
                "response_time": response_time,
                "timestamp": datetime.now().isoformat(),
                "model": self.model,
                "temperature": self.temperature,
                "scraped_urls": scraped_urls,
                "scraped_rating": scraped_rating
            }
            
            logger.info(f"Response generated successfully in {response_time:.2f}s")
            
            return {
                "content": response_text,
                "metadata": metadata
            }
        
        except ChatbotLLMException as e:
            logger.error(f"LLM error: {str(e)}")
            return self._create_error_response(str(e), start_time)
        
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            logger.error(error_msg)
            return self._create_error_response(error_msg, start_time)
    
    def _create_error_response(self, error_msg: str, start_time: float) -> Dict[str, Any]:
        """
        Create error response dictionary
        
        Args:
            error_msg: Error message
            start_time: Response start time
        
        Returns:
            Error response dictionary
        """
        error_response = f"I encountered an error processing your request: {error_msg}"
        return {
            "content": error_response,
            "metadata": {
                "sentiment": "negative",
                "confidence": 0.0,
                "length": len(error_response),
                "response_time": time.time() - start_time,
                "error": error_msg,
                "scraped_urls": [],
                "scraped_rating": None
            }
        }
    
    def _build_context(self) -> str:
        """
        Build context from recent conversation history
        
        Returns:
            Formatted context string
        """
        try:
            if not self.conversation_history:
                return ""
            
            # Use last 4 exchanges (8 messages max)
            recent_history = self.conversation_history[-8:]
            
            context = "Recent conversation context:\n"
            for msg in recent_history:
                role = "User" if msg["role"] == "user" else "Assistant"
                content = msg['content'][:200] + "..." if len(msg['content']) > 200 else msg['content']
                context += f"{role}: {content}\n"
            
            logger.debug(f"Context built from {len(recent_history)} recent messages")
            return context
        
        except Exception as e:
            logger.error(f"Error building context: {str(e)}")
            return ""
    
    def reset_history(self) -> None:
        """Clear conversation history"""
        try:
            self.conversation_history = []
            logger.info("Conversation history cleared")
        except Exception as e:
            logger.error(f"Error resetting history: {str(e)}")
    
    def get_history(self) -> List[Dict]:
        """
        Get full conversation history
        
        Returns:
            List of conversation messages
        """
        try:
            logger.debug(f"Retrieving conversation history ({len(self.conversation_history)} messages)")
            return self.conversation_history
        except Exception as e:
            logger.error(f"Error retrieving history: {str(e)}")
            return []
