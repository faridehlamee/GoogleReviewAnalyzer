#!/usr/bin/env python3
"""
Railway Startup Script for Google Review Analyzer
"""
import os
import sys
import subprocess

def main():
    """Main startup function"""
    print("🚂 Starting Google Review Analyzer on Railway...")
    
    # Check if Google API key is set
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY environment variable not set!")
        print("Please set your Google API key in Railway's Variables section")
        sys.exit(1)
    
    print(f"✅ Google API key found: {api_key[:10]}...")
    
    # Get port from Railway
    port = os.environ.get('PORT', '5008')
    print(f"🌐 Starting server on port {port}")
    
    # Start the Flask app
    try:
        from advanced_google_scraper import app
        app.run(host='0.0.0.0', port=int(port), debug=False)
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
