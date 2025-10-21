# 🧪 Testing Guide for Yelp Review Analyzer

This guide shows you how to test your Yelp Review Analyzer system at different levels.

## 🚀 Quick Start Testing

### Option 1: Quick Test (No API Key Required)
```bash
python quick_test.py
```
This runs a fast test with simulated data to verify the system works.

### Option 2: Full Test Suite
```bash
python test_analyzer.py
```
This runs comprehensive tests including mock data and real API tests.

## 📋 Test Categories

### 1. **Unit Tests** (No API Key Required)
Tests individual components:
- Configuration loading
- Error handling
- Data processing logic
- Visualization functions

### 2. **Integration Tests** (API Key Required)
Tests with real Yelp API:
- Business search functionality
- Review fetching
- API rate limiting
- Error handling

### 3. **Mock Tests** (No API Key Required)
Tests with simulated data:
- Complete analysis workflow
- User pattern detection
- Report generation
- Visualization creation

## 🛠️ Testing Methods

### Method 1: Quick Test
```bash
# Run quick test with simulated data
python quick_test.py
```

**What it tests:**
- ✅ Basic analyzer functionality
- ✅ Mock data processing
- ✅ User analysis logic
- ✅ Visualization creation
- ✅ Report generation

**Expected output:**
```
🚀 QUICK TEST - Yelp Review Analyzer
==================================================
📊 Running analysis...

YELP REVIEW ANALYSIS SUMMARY
==================================================
Business ID: test_business
Total Reviews Analyzed: 5
Reviews with Low Ratings (< 4 stars): 2
Suspicious Users Identified: 2

SUSPICIOUS REVIEWERS:
- Disappointed Customer (ID: user3)
  • Total Reviews: 6
  • Low Rating Percentage: 100.0%
  • Average Rating Given: 1.5/5.0
  • Rating for This Business: 2/5.0
  • Comment: "Poor service, food was cold"

- Angry Customer (ID: user4)
  • Total Reviews: 8
  • Low Rating Percentage: 87.5%
  • Average Rating Given: 1.4/5.0
  • Rating for This Business: 1/5.0
  • Comment: "Terrible experience, avoid this place"

📈 Testing visualizer...
✅ Visualizer test successful!

🎉 Quick test completed!
```

### Method 2: Full Test Suite
```bash
# Run comprehensive test suite
python test_analyzer.py
```

**What it tests:**
- ✅ Configuration loading
- ✅ API key validation
- ✅ Mock data analysis
- ✅ Business search functionality
- ✅ Visualization components
- ✅ Integration with real API (if key available)

### Method 3: Manual Testing

#### Test 1: Configuration Test
```python
from config import LOW_RATING_THRESHOLD, SUSPICIOUS_THRESHOLD
print(f"Low rating threshold: {LOW_RATING_THRESHOLD}")
print(f"Suspicious threshold: {SUSPICIOUS_THRESHOLD}")
```

#### Test 2: Business Search Test
```python
from utils import search_businesses
businesses = search_businesses("Starbucks", "New York, NY")
print(f"Found {len(businesses)} businesses")
```

#### Test 3: Analysis Test
```python
from yelp_analyzer import YelpReviewAnalyzer
analyzer = YelpReviewAnalyzer()
results = analyzer.analyze_business_reviews("your_business_id")
```

## 🔧 Testing with Real Data

### Step 1: Get Your API Key
1. Go to [Yelp Developers](https://www.yelp.com/developers/documentation/v3/authentication)
2. Create account and get API key
3. Add to `.env` file:
   ```
   YELP_API_KEY=your_actual_api_key_here
   ```

### Step 2: Test Business Search
```bash
python utils.py
```
This will let you interactively search for businesses.

### Step 3: Test Full Analysis
```bash
python main.py <business_id>
```

### Step 4: Test with Examples
```bash
python example_usage.py
```

## 🐛 Troubleshooting Tests

### Common Issues and Solutions

#### Issue 1: "No module named 'requests'"
```bash
pip install -r requirements.txt
```

#### Issue 2: "API key not found"
- Check if `.env` file exists
- Verify API key is set correctly
- Run `python setup.py` to create `.env` file

#### Issue 3: "No businesses found"
- Check if business ID is correct
- Verify API key has proper permissions
- Try a different business ID

#### Issue 4: "Import errors"
```bash
# Make sure you're in the correct directory
cd YelpReviewAnalyser

# Install dependencies
python setup.py
```

### Test Results Interpretation

#### ✅ All Tests Pass
Your system is working correctly and ready to use!

#### ⚠️ Some Tests Fail
Check the error messages and:
1. Install missing dependencies
2. Check configuration files
3. Verify API key setup
4. Review error logs

#### ❌ Integration Tests Fail
This is normal if you don't have an API key. The mock tests should still pass.

## 📊 Test Data Examples

### Sample Business IDs for Testing
```
# Well-known businesses (replace with actual IDs from your search)
Starbucks: 4kMBvIEWPxWkWKFN__8SxQ
McDonald's: WavJBJhJ2vJ1TpJ9JpJ9Jp
Pizza Hut: 7JpJ9JpJ9JpJ9JpJ9JpJ9
```

### Expected Test Outputs

#### Successful Analysis Output:
```
YELP REVIEW ANALYSIS SUMMARY
==================================================
Business ID: your_business_id
Total Reviews Analyzed: 50
Reviews with Low Ratings (< 4 stars): 8
Suspicious Users Identified: 2

SUSPICIOUS REVIEWERS:
- [User details with analysis]
- [Recommendations]

✅ Analysis complete!
Check the 'output' and 'reports' directories for detailed results.
```

## 🎯 Testing Checklist

Before using in production, verify:

- [ ] Quick test passes (`python quick_test.py`)
- [ ] Full test suite passes (`python test_analyzer.py`)
- [ ] Configuration loads correctly
- [ ] Business search works (if API key available)
- [ ] Analysis produces expected results
- [ ] Reports are generated properly
- [ ] Visualizations create successfully
- [ ] Error handling works correctly

## 🚀 Next Steps After Testing

Once tests pass:

1. **Get a real API key** for production use
2. **Test with real business data**
3. **Customize configuration** for your needs
4. **Run analysis on your target business**
5. **Review and act on results**

## 📞 Getting Help

If tests fail:
1. Check the error messages carefully
2. Verify all dependencies are installed
3. Ensure configuration files are correct
4. Review the troubleshooting section above
5. Check that you're using the correct Python version (3.8+)

Happy testing! 🎉
