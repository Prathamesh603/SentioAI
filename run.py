#!/usr/bin/env python3
"""
Run the Sentiment Analysis Chatbot Dashboard
Entry point for starting the Streamlit web application
"""

import subprocess
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
os.chdir(project_root)

if __name__ == "__main__":
    """Start the Streamlit dashboard"""
    
    print("=" * 60)
    print("Starting Sentiment Analysis Chatbot Dashboard...")
    print("=" * 60)
    print()
    
    # Run streamlit app
    streamlit_app = project_root / "dashboard" / "main.py"
    
    if not streamlit_app.exists():
        print(f"Error: Dashboard file not found at {streamlit_app}")
        sys.exit(1)
    
    print(f"Dashboard file: {streamlit_app}")
    print(f"Logs will be saved in: {project_root / 'logs'}")
    print()
    print("Opening dashboard in browser...")
    print("Press Ctrl+C to stop the server")
    print()
    
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(streamlit_app)],
            cwd=str(project_root)
        )
    except KeyboardInterrupt:
        print("\n\nDashboard stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting dashboard: {str(e)}")
        print("\nMake sure you have installed all dependencies:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
