# Sentiment Analysis Chatbot

A professional chatbot application with LangChain integration and web scraping capabilities. This project provides a beautiful Streamlit dashboard for interacting with an AI-powered sentiment analysis chatbot that can scrape product information from URLs.

## Features

✨ **Core Features:**
- 🤖 AI-powered chatbot using Groq's LLaMA model via LangChain
- 🌐 Web scraping for product info, reviews, and ratings
- 📊 Real-time sentiment analysis and quality metrics
- 💬 Conversation history with context awareness
- ⚙️ Adjustable response creativity (temperature)
- 📈 Performance analytics and tracking

🛡️ **Code Quality:**
- Custom logging system with file and console output
- Comprehensive exception handling
- Proper project structure following LangChain best practices
- Type hints throughout the codebase
- Modular, maintainable architecture

## Project Structure

```
sentiment_analysis_chatbot/
├── core/                    # Core utilities
│   ├── exceptions.py        # Custom exception classes
│   ├── logger.py            # Logging configuration
│   └── __init__.py
│
├── scrapers/               # Web scraping module
│   ├── product_scraper.py  # Product data scraper with logging
│   └── __init__.py
│
├── chatbot/                # Chatbot core module
│   ├── chatbot.py          # Main ChatBot class
│   └── __init__.py
│
├── utils/                  # Utility functions
│   ├── sentiment.py        # Sentiment analysis
│   ├── text_utils.py       # Text processing
│   ├── formatting.py       # Response formatting
│   └── __init__.py
│
├── metrics/                # Performance tracking
│   ├── tracker.py          # MetricsTracker class
│   └── __init__.py
│
├── dashboard/              # Streamlit UI
│   ├── main.py            # Main dashboard application
│   └── __init__.py
│
├── config.py              # Configuration constants
├── requirements.txt       # Project dependencies
├── .env.example          # Environment variables template
├── run.py                # Application entry point
└── __init__.py           # Package init
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone/Setup Project
```bash
cd sentiment_analysis_chatbot
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Groq API key
# Get it from: https://console.groq.com/keys
```

Example `.env` file:
```
GROQ_API_KEY=your_actual_groq_api_key_here
LOG_LEVEL=INFO
```

## Usage

### Run the Dashboard
```bash
python run.py
```

This will start the Streamlit dashboard at `http://localhost:8501`

### Using the Chatbot

1. **Simple Chat**: Type any message and the chatbot will respond
2. **Scrape Products**: Include a URL in your message (e.g., "https://amazon.com/...") to scrape product data
3. **Adjust Creativity**: Use the Temperature slider in the sidebar (0 = focused, 1 = creative)
4. **View Metrics**: Right panel shows real-time performance metrics
5. **Clear History**: Click the "Clear History" button to start fresh

## Logging

Logs are automatically saved in the `logs/` directory with:
- **Console output**: INFO level and above
- **File output**: DEBUG level and above with detailed information

Log files are organized by date and automatically rotated when they exceed 10MB.

Example log file: `logs/sentiment_analysis_chatbot_20240411.log`

## Configuration

### Model Settings
Edit `config.py` to customize:
- Temperature (0.0-1.0): Response creativity
- Max context turns: Conversation history length
- Chat model: Default uses LLaMA 3.3 70B

### UI Configuration
Modify `config.py` for:
- Page layout and styling
- Sentiment colors and emojis
- Display preferences

## Exception Handling

The application includes custom exceptions for:
- **ScraperException**: Web scraping errors
- **ChatbotLLMException**: LLM API errors
- **ConfigurationException**: Configuration issues
- **APIKeyException**: Missing/invalid API keys
- **ValidationException**: Data validation errors

All errors are logged automatically with full stack traces.

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.28.1 | Web UI framework |
| langchain | 0.1.0 | LLM orchestration |
| langchain-groq | 0.0.1 | Groq API integration |
| langchain-core | 0.1.0 | LangChain core |
| python-dotenv | 1.0.0 | Environment variables |
| requests | 2.31.0 | HTTP requests |
| beautifulsoup4 | 4.12.2 | HTML parsing |

## Troubleshooting

### "GROQ_API_KEY not found"
- Check your `.env` file exists and contains the key
- Make sure you're in the project root directory
- The key should be your actual Groq API key (not placeholder text)

### Scraper returns no data
- Some websites block automated scrapers
- Website HTML structure may have changed
- Try a different URL with a clearer structure

### Slow response times
- Temperature slider affects response length (higher = longer)
- API latency depends on Groq service
- Check your internet connection

### Port 8501 already in use
```bash
streamlit run dashboard/main.py --server.port=8502
```

## Development

### Adding New Features

1. **Add Scraper**: Extend `scrapers/product_scraper.py`
2. **Add Utils**: Create new file in `utils/` with logging
3. **Add Middleware**: Extend `core/` with new utilities

### Testing
```bash
# Test imports
python -c "from sentiment_analysis_chatbot import ChatBot; print('✅ Imports OK')"

# Test logging
python -c "from core.logger import setup_logger; logger = setup_logger('test'); logger.info('Test log')"
```

## Best Practices

✅ **Always use:**
- Logger for all operations: `logger.info()`, `logger.error()`
- Try-except blocks with proper exception types
- Type hints in function signatures
- Docstrings for all functions

❌ **Avoid:**
- Print statements (use logger instead)
- Bare except clauses
- Modifying log files directly
- Hardcoding configuration values

## Performance Tips

- 🚀 Keep context turns modest (4-5) for faster processing
- 📦 Use temperature 0.3-0.5 for consistent responses
- 🔍 Scrape URLs separately rather than in every message
- 💾 Clear history periodically for better performance

## Support & Documentation

- **Groq Documentation**: https://console.groq.com/docs
- **LangChain Docs**: https://python.langchain.com/
- **Streamlit Docs**: https://docs.streamlit.io/

## License

This project is provided as-is for educational and commercial use.

## Changelog

### Version 1.0.0 (Initial Release)
- Full chatbot functionality with LangChain
- Web scraping with multiple fallbacks
- Custom logging and exception handling
- Beautiful Streamlit dashboard
- Performance metrics and analytics
- Comprehensive error handling

---

**Last Updated**: April 2024  
**Status**: Production Ready ✅
