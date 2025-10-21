# 🚀 Google Places Review Analyzer - Setup Guide

## ✅ Successfully Converted to Google Places API!

Your Yelp Review Analyzer has been successfully converted to use Google Places API instead of Yelp. Here's everything you need to know:

## 🎯 What Changed

### ✅ **Updated Components:**
- **Main Analyzer**: Now uses Google Places API
- **Configuration**: Updated for Google API settings
- **Utils**: Updated for Google Places business search
- **Main Script**: Updated to work with place IDs
- **Dependencies**: Added Google Maps library

### ✅ **Benefits of Google Places API:**
- **FREE TIER**: 1,000 requests per month
- **Low Cost**: $5 per 1,000 additional requests (vs Yelp's $229/month minimum)
- **Good Review Data**: Access to Google reviews
- **Reliable**: Well-documented and stable API

## 🔑 Getting Your Google Places API Key

### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable billing (required even for free tier)

### Step 2: Enable Places API
1. In the Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Places API"
3. Click on "Places API" and click "Enable"

### Step 3: Create API Key
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "API Key"
3. Copy your API key
4. (Optional) Restrict the key to Places API for security

### Step 4: Configure Your Project
1. Copy `env_example.txt` to `.env`
2. Add your API key:
   ```
   GOOGLE_API_KEY=your_actual_google_api_key_here
   ```

## 🧪 Testing Your Setup

### Test 1: Quick Test (No API Key Required)
```bash
python test_google_analyzer.py
```

### Test 2: Business Search Test (API Key Required)
```bash
python utils.py
```

### Test 3: Full Analysis Test (API Key Required)
```bash
python main.py <place_id>
```

## 📊 How to Use

### Method 1: Find Place ID First
```bash
# Interactive search
python utils.py

# Then analyze
python main.py <place_id>
```

### Method 2: Direct Analysis
```bash
# Use a known place ID
python main.py ChIJN1t_tDeuEmsRUsoyG83frY4
```

### Method 3: Programmatic Usage
```python
from yelp_analyzer import GooglePlacesReviewAnalyzer

analyzer = GooglePlacesReviewAnalyzer()
results = analyzer.analyze_business_reviews("place_id_here")
print(analyzer.generate_summary_report(results))
```

## 🔍 Finding Place IDs

### Method 1: Interactive Search
```bash
python utils.py
# Follow prompts to search for businesses
```

### Method 2: Google Maps
1. Go to Google Maps
2. Search for a business
3. Click on the business
4. Look at the URL - the place ID is in the URL
5. Or use browser developer tools to find it

### Method 3: Programmatic Search
```python
from utils import search_businesses

businesses = search_businesses("Starbucks", "New York, NY")
place_id = businesses[0]['place_id']
```

## 💰 Cost Comparison

| Service | Free Tier | Additional Cost | Monthly Minimum |
|---------|-----------|----------------|-----------------|
| **Yelp API** | ❌ None | $5.91/1K calls | $229/month |
| **Google Places** | ✅ 1K calls | $5/1K calls | $0/month |

## 📈 What You Get

### ✅ **Same Analysis Features:**
- Identify suspicious reviewers
- Analyze review patterns
- Generate detailed reports
- Create visualizations
- Export data to CSV/JSON

### ✅ **Updated for Google Places:**
- Uses Google Places API
- Works with place IDs
- Accesses Google reviews
- Maintains all original functionality

## 🛠️ File Structure

```
YelpReviewAnalyser/
├── yelp_analyzer.py          # Main analyzer (now uses Google Places)
├── utils.py                  # Google Places business search
├── main.py                   # Command line interface
├── config.py                 # Google API configuration
├── test_google_analyzer.py   # Test script
├── requirements.txt          # Updated dependencies
├── .env                      # Your API key (create from env_example.txt)
└── README.md                 # Updated documentation
```

## 🎉 Ready to Use!

Your system is now ready to use with Google Places API:

1. **Get your API key** from Google Cloud Console
2. **Add it to .env file**
3. **Run the analyzer** on any business!

### Quick Start:
```bash
# 1. Set up API key
echo "GOOGLE_API_KEY=your_key_here" > .env

# 2. Test the system
python test_google_analyzer.py

# 3. Find a business
python utils.py

# 4. Analyze it
python main.py <place_id>
```

## 🔧 Troubleshooting

### Common Issues:

#### "No API key found"
- Make sure you created `.env` file
- Check that `GOOGLE_API_KEY=your_key` is in the file

#### "Places API not enabled"
- Go to Google Cloud Console
- Enable Places API for your project

#### "Billing required"
- Google requires billing to be enabled even for free tier
- You won't be charged for the first 1,000 requests per month

#### "No businesses found"
- Check your search terms
- Try different location formats
- Verify your API key has proper permissions

## 🎯 Success!

Your Yelp Review Analyzer is now successfully converted to use Google Places API and is ready to help you identify suspicious reviewers with a much more cost-effective solution!

**Next Steps:**
1. Get your Google Places API key
2. Test the system
3. Start analyzing businesses
4. Enjoy the free tier and low costs!

The system works exactly the same as before, but now uses Google's more affordable API! 🎉
