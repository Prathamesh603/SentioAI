"""
Main Streamlit dashboard application for the sentiment analysis chatbot
Provides web UI with chat interface, metrics, and analytics
"""

import os
import sys
import streamlit as st
import json
import re
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from core.logger import setup_logger, get_logger
from chatbot import ChatBot
from metrics import MetricsTracker
from utils import format_response, get_sentiment_color

# Setup main logger with static name
logger = setup_logger("applog", log_level="INFO")

# Page Configuration
st.set_page_config(
    page_title="Professional Chatbot Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

logger.info("Dashboard application started")

# Initialize Session State
if "chatbot" not in st.session_state:
    try:
        st.session_state.chatbot = ChatBot()
        st.session_state.metrics = MetricsTracker()
        st.session_state.messages = []
        logger.info("Session state initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing session state: {str(e)}")
        st.error(f"Error initializing chatbot: {str(e)}")
        st.stop()

chatbot = st.session_state.chatbot
metrics = st.session_state.metrics
messages = st.session_state.messages

st.markdown("""
<style>
/* Reduce top padding */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
}

/* Reduce title margin */
h1 {
    margin-top: 0px !important;
    margin-bottom: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR - HISTORY & SETTINGS ====================
with st.sidebar:
    st.title("☰ Menu")
    
    # Settings Section
    st.markdown("### ⚙️ Settings")
    
    model_temp = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Lower = focused, Higher = creative"
    )
    chatbot.set_temperature(model_temp)
    
    st.markdown("---")
    
    # Session Stats
    st.markdown("### 📊 Stats")
    metrics_summary = metrics.get_metrics_summary()
    st.metric("Messages", len(messages))
    st.metric("Avg Time", f"{metrics_summary['avg_response_time']:.2f}s")
    
    st.markdown("---")
    
    # Clear Button
    if st.button("🔄 Clear History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.metrics = MetricsTracker()
        logger.info("User cleared chat history")
        st.rerun()
    
    st.markdown("---")
    
    # Conversation History
    st.markdown("### 📜 History")
    
    if messages:
        for i, msg in enumerate(messages):
            if msg["role"] == "user":
                preview = msg['content'][:40] + "..." if len(msg['content']) > 40 else msg['content']
                st.markdown(f"""
                <div style='background-color: blue; padding: 8px; border-radius: 6px; margin: 4px 0; font-size: 11px; border-left: 3px solid #2196F3; color: black;'>
                    <b>You:</b> {preview}
                </div>
                """, unsafe_allow_html=True)
            else:
                preview = msg['content'][:40] + "..." if len(msg['content']) > 40 else msg['content']
                st.markdown(f"""
                <div style='background-color: white; padding: 8px; border-radius: 6px; margin: 4px 0; font-size: 11px; border-left: 3px solid #4CAF50; color: black;'>
                    <b>🤖:</b> {preview}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No conversations yet", icon="💬")

# ==================== MAIN AREA - TWO COLUMNS ====================
st.title("SentioAI")

# Create two columns: Left (Chat) | Right (Analytics)
col_chat, col_analytics = st.columns([3.5, 1])

# ==================== LEFT COLUMN - CHAT INTERFACE ====================
with col_chat:
    # Chat display area (scrollable)
    with st.container(height=500, border=False):
        if messages:
            for msg in messages:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div style='text-align: right; margin: 8px 0;'>
                        <div style='display: inline-block; background-color: #2a2a2a; color: white; font-family: Arial, sans-serif; padding: 10px 14px; border-radius: 18px; max-width: 75%; text-align: left; word-wrap: break-word; border-bottom-right-radius: 4px;'>
                            {msg['content']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Assistant response - clean and simple
                    st.markdown(f"""
                    <div style='text-align: left; margin: 8px 0;'>
                        <div style='display: inline-block; background-color: #2a2a2a; color: white; font-family: Arial, sans-serif; padding: 10px 14px; border-radius: 18px; max-width: 75%; text-align: left; word-wrap: break-word; border-bottom-left-radius: 4px; line-height: 1.6;'>
                            {msg['content']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='text-align: center; padding: 100px 20px; color: #999;'>
                <h3>Hi there! 👋</h3>
                <p>Start a conversation by typing a message below</p>
            </div>
            """, unsafe_allow_html=True)
    
    # ==================== INPUT AREA AT BOTTOM ====================
    st.markdown("")
    
    col_input, col_btn = st.columns([5, 1])
    
    with col_input:
        user_input = st.text_input(
            "Message",
            placeholder="Type your message here...",
            label_visibility="collapsed",
            key="user_message"
        )
    
    with col_btn:
        send_button = st.button("Send", use_container_width=True, key="send_btn")
    
    # Process Message
    if send_button and user_input.strip():
        try:
            # Add user message
            messages.append({"role": "user", "content": user_input})
            logger.info(f"User message received: {user_input[:100]}...")
            
            # Check if user provided a URL for scraping
            url_pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
            urls_found = re.findall(url_pattern, user_input)
            
            if urls_found:
                with st.spinner(f"🔍 Scraping data from {len(urls_found)} URL(s)... This may take a moment."):
                    logger.info(f"Found {len(urls_found)} URLs in user input, starting scrape...")
                    
                    # Get bot response (which includes scraping)
                    response = chatbot.generate_response(user_input)
                    
                    # Check if data was scraped
                    scraped_urls = response["metadata"].get("scraped_urls", [])
                    if scraped_urls:
                        # Check if actual data exists
                        scraped_success = False
                        for url in scraped_urls:
                            if url in chatbot.scraped_data:
                                data = chatbot.scraped_data[url]
                                if data.get("scraped", False):
                                    scraped_success = True
                                    st.success(f"✅ Successfully scraped: {url}")
                                    logger.info(f"Successfully scraped: {url}")
                                else:
                                    st.warning(f"⚠️ Scraping returned no data from: {url}\n**This might mean:** The website structure changed, blocked the request, or the content isn't available.")
                                    logger.warning(f"No data scraped from: {url}")
                    
                    # Calculate metrics
                    metrics.add_response(user_input, response["content"], response["metadata"])
                    logger.info(f"Response generated in {response['metadata']['response_time']:.2f}s")
            
            else:
                with st.spinner("💭 Thinking..."):
                    logger.info("Processing user message without URL...")
                    
                    # Get bot response
                    response = chatbot.generate_response(user_input)
                    
                    # Calculate metrics
                    metrics.add_response(user_input, response["content"], response["metadata"])
                    logger.info(f"Response generated in {response['metadata']['response_time']:.2f}s")
            
            # Add bot message with metadata
            messages.append({
                "role": "assistant",
                "content": response["content"],
                "metadata": response["metadata"]
            })
            
            logger.info("Message processed successfully")
            st.rerun()
        
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            st.error(f"Error processing your message: {str(e)}")

# ==================== RIGHT COLUMN - ANALYTICS & RATING ====================
with col_analytics:
    st.markdown("### 📊 Rating")
    
    try:
        # Check if there's a scraped rating from the URL
        scraped_rating = None
        count_rating = 0
        for url, data in chatbot.scraped_data.items():
            if data.get("rating") is not None:
                count_rating += 1
                scraped_rating = data.get("rating")
                if(count_rating < 2):
                    st.info(f"⭐ **Product Rating (from URL)**")
                
        
        # Get metrics
        metrics_summary = metrics.get_metrics_summary()
        rating = metrics.get_overall_rating()
        
        # Display scraped rating if available, otherwise show calculated rating
        if scraped_rating is not None:
            display_rating = scraped_rating
            rating_label = "Product Rating (Scraped)"
            color = "#FF9800"  # Orange for scraped data
        else:
            display_rating = rating
            rating_label = "Quality Score (Calculated)"
            color = "#4CAF50"  # Green for calculated
        
        # Overall Rating Display
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, {color}, {color}dd); border-radius: 12px; color: white;'>
            <div style='font-size: 48px; font-weight: bold; margin: 10px 0;'>{display_rating:.1f}</div>
            <div style='font-size: 12px; opacity: 0.9;'>{rating_label}</div>
            <div style='font-size: 20px; margin-top: 10px;'>{"⭐" * int(display_rating)}{"☆" * (5 - int(display_rating))}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        # Metrics Breakdown
        st.markdown("#### Key Metrics")
        
        st.metric("Total Messages", len(messages), help="Messages exchanged")
        st.metric("Avg Response", f"{metrics_summary['avg_response_time']:.2f}s", help="Average response time")
        st.metric("Avg Length", f"{int(metrics_summary['avg_response_length'])}", help="Avg characters per response")
        
        st.markdown("")
        
        # Sentiment Analysis
        st.markdown("#### Sentiment")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Positive", metrics_summary.get('positive_sentiment', 0))
            st.metric("Negative", metrics_summary.get('negative_sentiment', 0))
        
        with col2:
            st.metric("Neutral", metrics_summary.get('neutral_sentiment', 0))
            st.metric("Confidence", f"{metrics_summary.get('avg_confidence', 0):.0%}")
        
        st.markdown("")
        
        # Last Response Details
        if messages and messages[-1]["role"] == "assistant":
            st.markdown("#### Last Response")
            
            last_meta = messages[-1].get("metadata", {})
            
            sent = last_meta.get('sentiment', 'N/A').upper()
            conf = f"{last_meta.get('confidence', 0):.0%}"
            resp_time = f"{last_meta.get('response_time', 0):.2f}s"
            length = f"{last_meta.get('length', 0)}"
            scraped_rating_data = last_meta.get('scraped_rating', None)
            
            # Build details with scraped rating if available
            details = f"""
            <div style='background: #f5f5f5; padding: 12px; border-radius: 8px; font-size: 13px; line-height: 1.8; color: black;'>
                <b>Sentiment:</b> {sent}<br>
                <b>Confidence:</b> {conf}<br>
                <b>Time:</b> {resp_time}<br>
                <b>Length:</b> {length} chars
            """
            
            if scraped_rating_data:
                details += f"<br><b>Rating:</b> ⭐ {scraped_rating_data}/5"
            
            details += "</div>"
            
            st.markdown(details, unsafe_allow_html=True)
    
    except Exception as e:
        logger.error(f"Error displaying analytics: {str(e)}")
        st.error("Error loading analytics")

logger.info("Dashboard rendered successfully")
