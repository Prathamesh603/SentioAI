# Sentiment Analysis Chatbot - Setup Guide

Complete step-by-step guide to get the chatbot up and running.

## ⚡ Quick Start (5 minutes)

### 1. Verify Python Installation
```bash
python --version  # Should be 3.8 or higher
```

### 2. Navigate to Project
```bash
cd sentiment_analysis_chatbot
```

### 3. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Setup Environment Variables
```bash
# Copy template
cp .env.example .env

# Edit .env (on Windows use notepad .env)
# Add your Groq API key from https://console.groq.com/keys
```

### 6. Run the Application
```bash
python run.py
```

Dashboard will open at: **http://localhost:8501**

---

## 📋 Detailed Setup

### Prerequisites Check
- ✅ Python 3.8+ installed
- ✅ pip package manager available
- ✅ Internet connection for API calls
- ✅ Groq API key (free from https://console.groq.com)

### Step-by-Step Installation

#### Step 1: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

*You should see `(venv)` at the start of your terminal prompt*

#### Step 2: Upgrade pip (Optional but Recommended)
```bash
pip install --upgrade pip
```

#### Step 3: Install Requirements
```bash
pip install -r requirements.txt
```

*This installs all dependencies: streamlit, langchain, requests, beautifulsoup4, dotenv*

#### Step 4: Get Groq API Key

1. Go to https://console.groq.com/keys
2. Sign up (free account)
3. Create an API key
4. Copy the key (looks like: `gsk_...`)

#### Step 5: Configure Environment

**Create .env file:**
```bash
cp .env.example .env
```

**Edit .env file:**
```
GROQ_API_KEY=gsk_your_actual_key_here
LOG_LEVEL=INFO
```

*Save the file*

#### Step 6: Verify Installation
```bash
# Test imports
python -c "import streamlit, langchain, requests; print('✅ All imports OK')"

# Test configuration
python -c "from sentiment_analysis_chatbot import ChatBot; print('✅ ChatBot imports OK')"
```

#### Step 7: Run the Application
```bash
python run.py
```

*The dashboard will automatically open in your browser*

---

## 🎯 First Use

### Dashboard Layout

```
┌─────────────────────────────────────┬──────────────┐
│                                     │              │
│      CHAT INTERFACE                 │  ANALYTICS   │
│  (Main conversation area)           │              │
│                                     │   Rating     │
│  [Your messages]                    │   Metrics    │
│  [Bot responses]                    │   Sentiment  │
│                                     │              │
│  [Input box] [Send]                 │              │
├─────────────────────────────────────┴──────────────┤
│  SIDEBAR: Settings, History, Stats
└──────────────────────────────────────────────────────┘
```

### Using the Chatbot

1. **Type a message**
   ```
   "Hello! Tell me about AI"
   ```
   The chatbot will respond naturally.

2. **With product URL** (to scrape data)
   ```
   "What can you tell me about this product? https://amazon.com/..."
   ```
   The bot will scrape and analyze the product.

3. **Adjust settings** (in sidebar)
   - Temperature slider: 0 = precise, 1 = creative
   - Clear History: Start a new conversation

4. **View metrics** (right panel)
   - Overall rating
   - Response time
   - Sentiment analysis

---

## 🔧 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```bash
# Make sure you're in the project root
cd sentiment_analysis_chatbot

# Reinstall dependencies
pip install -r requirements.txt

# Verify
python -c "import streamlit; print(streamlit.__version__)"
```

### Problem: "GROQ_API_KEY not found in environment variables"

**Solution:**
1. Check that `.env` file exists in the project root
2. Open `.env` and verify it contains your API key:
   ```
   GROQ_API_KEY=gsk_your_actual_key_here
   ```
3. Make sure there are no quotes around the key
4. Restart the application: `python run.py`

### Problem: "Port 8501 is already in use"

**Solution:**
```bash
# Use a different port
streamlit run dashboard/main.py --server.port=8502
```

### Problem: Scraper returns no data

**Possible causes:**
1. Website blocks automated requests
2. Website structure changed
3. URL is not a product page
4. Website returns 403 Forbidden

**Solution:**
- Try different URLs
- Check if website is accessible in browser
- Use a URL with clear product information

### Problem: Slow responses

**Possible causes:**
1. High temperature setting (longer responses)
2. Network latency
3. Server processing time

**Solution:**
- Lower temperature slider
- Check internet connection
- Wait a bit for API response

### Problem: Cannot activate virtual environment

**Windows:**
```bash
# If venv\Scripts\activate doesn't work:
python -m venv venv
venv\Scripts\activate.ps1  # PowerShell
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

---

## 📁 Project Files Explained

```
sentiment_analysis_chatbot/
│
├── core/
│   ├── exceptions.py     # Custom error classes
│   ├── logger.py         # Logging configuration
│   └── __init__.py
│
├── scrapers/
│   ├── product_scraper.py    # Web scraper for product data
│   └── __init__.py
│
├── chatbot/
│   ├── chatbot.py        # Main chatbot class
│   └── __init__.py
│
├── utils/
│   ├── sentiment.py           # Sentiment analysis functions
│   ├── text_utils.py          # Text processing functions
│   ├── formatting.py          # Output formatting
│   └── __init__.py
│
├── metrics/
│   ├── tracker.py            # Performance metrics tracking
│   └── __init__.py
│
├── dashboard/
│   ├── main.py               # Streamlit dashboard
│   └── __init__.py
│
├── logs/                      # (Created automatically)
│   └── *.log                  # Log files
│
├── config.py                  # Configuration constants
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── .env                      # (Create this with your API key)
├── run.py                    # Application entry point
├── README.md                 # Full documentation
├── SETUP_GUIDE.md           # This file
└── __init__.py              # Package initialization
```

---

## ✅ Verification Checklist

Before using the application:

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip list`)
- [ ] `.env` file created with API key
- [ ] Can import modules: `python -c "from sentiment_analysis_chatbot import ChatBot"`
- [ ] Logs folder is readable/writable
- [ ] Internet connection available
- [ ] Port 8501 is available

---

## 🚀 Running the Application

### Standard Startup
```bash
python run.py
```

### Custom Port
```bash
streamlit run dashboard/main.py --server.port=8502
```

### Development Mode (with reload)
```bash
streamlit run dashboard/main.py --logger.level=debug
```

### Headless Mode (no browser)
```bash
streamlit run dashboard/main.py --server.headless=true
```

---

## 📊 Log Files

All application activity is logged to `logs/` directory:

```
logs/
├── sentiment_analysis_chatbot_20240411.log
├── sentiment_analysis_chatbot_20240410.log
└── ...
```

**Log Levels:**
- **DEBUG**: Detailed internal operations
- **INFO**: General information (default)
- **WARNING**: Warning messages
- **ERROR**: Error messages with stack traces

**View logs:**
```bash
# Windows
type logs\sentiment_analysis_chatbot_20240411.log

# macOS/Linux
cat logs/sentiment_analysis_chatbot_20240411.log

# Follow live logs (macOS/Linux)
tail -f logs/sentiment_analysis_chatbot_20240411.log
```

---

## 🎓 Next Steps

1. ✅ Setup complete!
2. 📖 Read [README.md](README.md) for full documentation
3. 🔍 Try the chatbot with different prompts
4. 🌐 Test with real product URLs
5. ⚙️ Adjust settings in `config.py` if needed

---

## 💡 Tips & Tricks

### Faster Responses
- Lower the temperature slider (more focused)
- Use shorter prompts
- Clear history periodically

### Better Scraping
- Use complete product URLs
- Try e-commerce sites first (Amazon, eBay)
- Include product name in your message

### Logging Details
- Check logs for debugging
- Increase LOG_LEVEL to DEBUG for more detail
- Log files auto-rotate at 10MB

---

## ❓ Support

If you encounter issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review log files in `logs/` directory
3. Verify `.env` file configuration
4. Test with `python -c "from sentiment_analysis_chatbot import ChatBot"`
5. Check internet connection
6. Verify API key is valid at https://console.groq.com/keys

---

**Setup Notes:**
- Project is production-ready ✅
- All dependencies are stable versions
- No breaking changes expected
- Logs are automatically cleaned up (5 backups)

**Last Updated**: April 2024
