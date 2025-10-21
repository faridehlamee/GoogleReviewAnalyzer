# 🔑 Yelp API Setup Guide

## How to Get Your API Key

### Step 1: Create Yelp Developer Account
1. Go to [Yelp Developers](https://www.yelp.com/developers/documentation/v3/authentication)
2. Click "Get Started" or "Create App"
3. Sign up with your email/password
4. Verify your email address

### Step 2: Create Your App
1. Fill out the app details:
   - **App Name**: "Yelp Review Analyzer" (or your choice)
   - **Description**: "Tool to analyze Yelp review patterns and identify suspicious reviewers"
   - **Website**: Your website or GitHub repo
   - **Category**: Choose appropriate category

### Step 3: Get Your API Key
1. After creating the app, you'll see your API key
2. Copy the key (it looks like: `Bearer abc123def456ghi789...`)
3. Add it to your `.env` file:
   ```
   YELP_API_KEY=your_actual_api_key_here
   ```

## What You Can Do with Your API Key

### ✅ Single Key = Access to All Businesses
```python
# One API key works for ALL businesses
analyzer = YelpReviewAnalyzer()

# Analyze any business on Yelp
businesses_to_analyze = [
    "starbucks_business_id",
    "mcdonalds_business_id", 
    "pizza_hut_business_id",
    "any_restaurant_business_id"
]

for business_id in businesses_to_analyze:
    results = analyzer.analyze_business_reviews(business_id)
    print(f"Analysis complete for {business_id}")
```

### ✅ Find Business IDs
```python
from utils import search_businesses

# Search for any business
businesses = search_businesses("Starbucks", "New York, NY")
print(f"Found {len(businesses)} Starbucks locations")

# Get business ID from search results
business_id = businesses[0]['id']
```

## API Usage Limits

### Free Tier Limits
- **500 requests per day**
- **5 requests per second**
- **Rate limiting**: Must wait between requests

### Your System Handles This
- ✅ **Automatic delays** between API calls
- ✅ **Rate limit compliance** built-in
- ✅ **Error handling** for limits
- ✅ **Efficient caching** to minimize requests

## Testing Your API Key

### Test 1: Basic Connection
```python
from utils import search_businesses

# Test with a simple search
businesses = search_businesses("Starbucks", "New York, NY")
if businesses:
    print("✅ API key is working!")
    print(f"Found {len(businesses)} businesses")
else:
    print("❌ API key not working or no results")
```

### Test 2: Full Analysis
```python
from yelp_analyzer import YelpReviewAnalyzer

analyzer = YelpReviewAnalyzer()
# Use a business ID from your search
results = analyzer.analyze_business_reviews("business_id_here")
print("Analysis complete!")
```

## Important Notes

### ✅ What You CAN Do
- Analyze reviews for any business on Yelp
- Identify suspicious reviewers
- Generate reports for multiple businesses
- Use the same API key for all analyses

### ❌ What You CANNOT Do
- Get complete review history for individual users
- Access private user information
- Bypass rate limits
- Use for commercial purposes without proper licensing

### ⚠️ Legal Considerations
- **Respect Yelp's Terms of Service**
- **Use data responsibly**
- **Don't violate user privacy**
- **Consider data protection laws**

## Ready to Use!

Once you have your API key:
1. Add it to `.env` file
2. Run: `python main.py <business_id>`
3. Analyze any business on Yelp!

Your single API key gives you access to analyze reviews for ANY business on Yelp! 🎉
