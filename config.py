"""
Configuration file for Google Places Review Analyzer
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Places API Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')

# Analysis Configuration
LOW_RATING_THRESHOLD = 4  # Stars below this are considered "low ratings"
MIN_REVIEWS_FOR_ANALYSIS = 5  # Minimum reviews a user needs to be analyzed
SUSPICIOUS_THRESHOLD = 0.7  # If 70%+ of reviews are low ratings, user is suspicious

# API Rate Limiting
REQUESTS_PER_SECOND = 10
DELAY_BETWEEN_REQUESTS = 0.1  # seconds

# Output Configuration
OUTPUT_DIR = 'output'
REPORTS_DIR = 'reports'
