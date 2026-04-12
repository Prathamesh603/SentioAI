"""
Configuration and Constants for Professional Chatbot Dashboard
"""

# UI Configuration
UI_CONFIG = {
    "page_title": "Professional Chatbot Dashboard",
    "page_icon": "🤖",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Chat Configuration
CHAT_CONFIG = {
    "model": "llama-3.3-70b-versatile",
    "api_provider": "groq",
    "base_url": "https://api.groq.com/openai/v1",
    "default_temperature": 0.7,
    "max_context_turns": 4,  # Number of conversation turns to keep in context
    "max_input_length": 5000,
    "max_output_length": 10000
}

# Metrics Configuration
METRICS_CONFIG = {
    "ideal_response_time": 2.0,  # seconds
    "ideal_response_length": (200, 500),  # characters range
    "ideal_input_length": (50, 200),  # characters range
    "quality_weights": {
        "speed": 0.33,
        "engagement": 0.33,
        "quality": 0.34
    }
}

# Display Configuration
DISPLAY_CONFIG = {
    "chat_history_height": 400,  # pixels
    "max_messages_display": 100,
    "message_preview_length": 500,  # truncate long messages in history
    "sentiment_emojis": {
        "positive": "😊",
        "negative": "😞",
        "neutral": "😐"
    },
    "sentiment_colors": {
        "positive": "#4CAF50",
        "negative": "#f44336",
        "neutral": "#FFC107"
    }
}
