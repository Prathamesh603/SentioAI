# Quick Reference Guide

A one-page reference for common tasks.

## Starting the App
```bash
python run.py
```

## Running Tests (Optional Setup)
```bash
# Test imports
python -c "from sentiment_analysis_chatbot import ChatBot; print('✅ OK')"

# Test logging
python -c "from core.logger import setup_logger; logger = setup_logger('test'); logger.info('Test')"
```

## Common Imports

### From Core
```python
from core.logger import setup_logger, get_logger
from core.exceptions import ChatbotException, APIKeyException
```

### From Chatbot
```python
from chatbot import ChatBot

bot = ChatBot()
response = bot.generate_response("Hello!")
```

### From Scrapers
```python
from scrapers import get_product_info, get_reviews, get_rating

info = get_product_info("https://example.com")
reviews = get_reviews("https://example.com")
rating = get_rating("https://example.com")
```

### From Utils
```python
from utils import (
    calculate_sentiment,
    format_response,
    extract_keywords,
    calculate_readability_score,
    get_sentiment_color,
    get_sentiment_emoji
)
```

### From Metrics
```python
from metrics import MetricsTracker

tracker = MetricsTracker()
tracker.add_response(input_text, response_text, metadata)
summary = tracker.get_metrics_summary()
```

## File Locations

| What | Where |
|------|-------|
| API Key | `.env` file |
| Logs | `logs/` directory (auto-created) |
| Config | `config.py` |
| Dashboard | `dashboard/main.py` |
| Entry Point | `run.py` |
| Documentation | `README.md` |

## Common Tasks

### Add Logging to Your Code
```python
from core.logger import get_logger

logger = get_logger(__name__)

logger.info("Info message")
logger.debug("Debug details")
logger.warning("Warning!")
logger.error("Error occurred")
```

### Handle Errors
```python
from core.exceptions import ChatbotException, APIKeyException

try:
    bot = ChatBot()
except APIKeyException as e:
    print(f"Missing API key: {e}")
except ChatbotException as e:
    print(f"Chatbot error: {e}")
```

### Get Metrics
```python
from metrics import MetricsTracker

tracker = MetricsTracker()
# ... (add responses)
summary = tracker.get_metrics_summary()
print(f"Rating: {summary['overall_rating']:.1f}")
print(f"Avg Time: {summary['avg_response_time']:.2f}s")
```

### Analyze Sentiment
```python
from utils import calculate_sentiment

text = "I love this product!"
sentiment, confidence = calculate_sentiment(text)
print(f"Sentiment: {sentiment} ({confidence:.0%} confident)")
```

## Configuration

### Change Temperature
In code:
```python
bot = ChatBot()
bot.set_temperature(0.3)  # More focused
```

Or in dashboard:
- Sidebar → Temperature slider

### Change Model Settings
Edit `config.py`:
```python
CHAT_CONFIG = {
    "model": "llama-3.3-70b-versatile",
    "default_temperature": 0.7,
    "max_context_turns": 4,
}
```

### Change Logging Level
In `.env`:
```
LOG_LEVEL=DEBUG  # More verbose
LOG_LEVEL=INFO   # Normal
LOG_LEVEL=WARNING # Less verbose
```

## Directory Structure Quick Reference

```
sentiment_analysis_chatbot/
├── core/              ← Logging, exceptions
├── scrapers/          ← Web scraping
├── chatbot/           ← Main ChatBot class
├── utils/             ← Helper functions
├── metrics/           ← Performance tracking
├── dashboard/         ← Streamlit UI
├── config.py          ← Configuration
├── run.py             ← Start here!
├── .env               ← Your API key
├── logs/              ← Log files (auto)
└── README.md          ← Full docs
```

## Environment Variables

```bash
# .env file format
GROQ_API_KEY=gsk_your_key_here
LOG_LEVEL=INFO
APP_NAME=Sentiment Analysis Chatbot
```

## Debugging

### Enable Debug Logging
```bash
# In .env
LOG_LEVEL=DEBUG

# Then restart
python run.py
```

### Check Logs
```bash
# View latest log
cat logs/sentiment_analysis_chatbot_*.log

# Follow live log (macOS/Linux)
tail -f logs/sentiment_analysis_chatbot_*.log
```

### Test API Key
```bash
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('GROQ_API_KEY')
print(f'Key exists: {bool(key)}')
print(f'Key starts with: {key[:10] if key else \"None\"}...')
"
```

## Tips

- 🚀 Start with `python run.py`
- 📝 Check logs in `logs/` for errors
- 🔑 Make sure `.env` has your API key
- 💾 Logs auto-rotate at 10MB
- 🔄 Clear history in sidebar to reset
- 🌡️ Lower temperature for consistent responses

## Shortcuts

| Command | What it does |
|---------|-------------|
| `python run.py` | Start dashboard |
| `pip install -r requirements.txt` | Install dependencies |
| `python -c "from sentiment_analysis_chatbot import ChatBot"` | Test imports |
| `cat logs/*.log` | View logs |
| `rm logs/*` | Clear logs |
| `deactivate` | Exit virtual environment |

## Troubleshooting Checklist

- [ ] Virtual environment activated? (`(venv)` in prompt)
- [ ] Dependencies installed? (`pip list | grep streamlit`)
- [ ] `.env` exists with API key?
- [ ] Port 8501 available?
- [ ] Internet connection? (for API calls)
- [ ] Logs folder readable/writable?

---

**Last Updated**: April 2024  
**Version**: 1.0.0
