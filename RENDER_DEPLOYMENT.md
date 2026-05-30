# Render Deployment Guide

## Pre-Deployment Checklist

✅ **Requirements Fixed**
- Removed triple quotes from `.env.example`
- Updated `requirements.txt` with all necessary dependencies
- Added comments for better readability

## Deploy to Render

### Step 1: Prepare Repository
```bash
git add .
git commit -m "Fix deployment: clean requirements.txt and config"
git push
```

### Step 2: Connect to Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select branch: `main`
5. Fill in details:
   - **Name**: `sentiment-analysis-chatbot`
   - **Environment**: Python
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run dashboard/main.py --server.port=$PORT --server.address=0.0.0.0`

### Step 3: Set Environment Variables

In Render Dashboard → Environment:

```
GROQ_API_KEY = your_api_key_here
LOG_LEVEL = INFO
PYTHONUNBUFFERED = 1
```

### Step 4: Deploy

Click **"Create Web Service"** and Render will deploy!

## Troubleshooting

### If deployment fails:

1. **Check build logs** - Look for any Python errors
2. **Verify GROQ_API_KEY** - Must be set in Render dashboard
3. **Port binding** - Ensure `--server.address=0.0.0.0` and `--server.port=$PORT` are in start command
4. **Requirements syntax** - Confirmed all lines are valid package specs

## Access Your App

After successful deployment:
- Your app will be available at: `https://your-app-name.onrender.com`
- Logs available in Render Dashboard

## Important Notes

- **Free tier**: Apps spin down after 15 min of inactivity
- **Logs**: Check Render dashboard for detailed deployment logs
- **Python version**: Using 3.11 (compatible with all dependencies)
- **Storage**: No persistent file system; use environment variables for sensitive data
