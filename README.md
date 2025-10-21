# YELP REVIEW ANALYZER
SOFTWARE TO ANALYZE YELP REVIEW PATTERNS AND IDENTIFY SUSPICIOUS REVIEWERS

## Overview
This project analyzes Yelp reviews to identify users who consistently give low ratings across multiple businesses, helping to detect potentially suspicious review patterns. It's designed to help business owners understand their review landscape and identify users who may be giving unfair or consistently negative reviews.

## 🎯 What It Does
1. **Fetches all reviews** for a target business with stars, comments, and reviewer names
2. **Identifies reviewers** who gave less than 4 stars to your business
3. **Analyzes review patterns** of these users across all their Yelp reviews
4. **Detects suspicious behavior** - users who consistently give low ratings
5. **Generates detailed reports** and visualizations

## 🚀 Quick Start

### 1. Setup
```bash
# Clone or download this project
cd YelpReviewAnalyser

# Run the setup script
python setup.py
```

### 2. Get Yelp API Key
1. Go to [Yelp Developers](https://www.yelp.com/developers/documentation/v3/authentication)
2. Create an account and get your API key
3. Edit the `.env` file and add your API key:
   ```
   YELP_API_KEY=your_actual_api_key_here
   ```

### 3. Run Analysis
```bash
# Find a business ID first
python utils.py

# Analyze a specific business
python main.py <business_id>

# Or run interactive examples
python example_usage.py
```

## 📊 Features

### Core Analysis
- **Review Collection**: Fetches all available reviews for a business
- **User Pattern Analysis**: Analyzes each reviewer's history across Yelp
- **Suspicious User Detection**: Identifies users with consistently low ratings
- **Statistical Analysis**: Calculates percentages, averages, and patterns

### Reporting & Visualization
- **Detailed Reports**: Text and JSON reports with analysis results
- **Interactive Dashboards**: Comprehensive visualizations of findings
- **CSV Export**: Export results for further analysis
- **Summary Statistics**: Key metrics and recommendations

### Configurable Parameters
- **Rating Thresholds**: Customize what constitutes a "low rating"
- **Suspicious Threshold**: Adjust sensitivity for detecting suspicious users
- **Rate Limiting**: Respects Yelp API limits

## 🛠️ Usage Examples

### Basic Analysis
```python
from yelp_analyzer import YelpReviewAnalyzer

analyzer = YelpReviewAnalyzer()
results = analyzer.analyze_business_reviews("your_business_id")

# Print summary
print(analyzer.generate_summary_report(results))
```

### With Visualizations
```python
from visualizer import YelpDataVisualizer

visualizer = YelpDataVisualinator()
visualizer.create_summary_dashboard(results)
```

### Find Business ID
```python
from utils import find_business_id

business_id = find_business_id("Starbucks", "New York, NY")
```

## 📁 Project Structure
```
YelpReviewAnalyser/
├── yelp_analyzer.py      # Main analysis engine
├── visualizer.py         # Data visualization tools
├── utils.py             # Utility functions
├── main.py              # Command line interface
├── example_usage.py     # Usage examples
├── setup.py             # Setup script
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── output/              # Analysis results
├── reports/             # Generated reports
└── README.md           # This file
```

## ⚙️ Configuration

Edit `config.py` to customize:
- `LOW_RATING_THRESHOLD`: Stars below this are "low ratings" (default: 4)
- `SUSPICIOUS_THRESHOLD`: Percentage of low ratings to flag as suspicious (default: 0.7)
- `MIN_REVIEWS_FOR_ANALYSIS`: Minimum reviews needed to analyze a user (default: 5)

## 📈 Understanding Results

### Suspicious User Criteria
A user is flagged as suspicious if:
- They gave your business less than 4 stars
- 70%+ of their total reviews are low ratings (< 4 stars)
- They have at least 5 total reviews

### Report Contents
- **User Analysis**: Individual user statistics and patterns
- **Rating Distributions**: Visual breakdowns of ratings
- **Recommendations**: Actionable insights based on findings
- **Summary Statistics**: Key metrics and trends

## ⚠️ Important Notes

### API Limitations
- Yelp API doesn't provide access to all reviews by a user
- The current implementation simulates user review data for demonstration
- In production, you would need to build a database over time or use other data sources

### Rate Limiting
- Respects Yelp API rate limits
- Includes delays between requests
- Handles API errors gracefully

### Legal Considerations
- Ensure compliance with Yelp's Terms of Service
- Use data responsibly and ethically
- Consider privacy implications when analyzing user data

## 🔧 Troubleshooting

### Common Issues
1. **API Key Error**: Make sure your Yelp API key is correctly set in `.env`
2. **No Reviews Found**: Check if the business ID is correct
3. **Import Errors**: Run `python setup.py` to install dependencies

### Getting Business IDs
1. Use the interactive search: `python utils.py`
2. Search on Yelp.com and extract ID from URL
3. Use the business search API

## 📝 License
This project is for educational and research purposes. Please ensure compliance with Yelp's Terms of Service and applicable laws when using this software.

## 🤝 Contributing
Feel free to submit issues, feature requests, or pull requests to improve this tool!

## 📞 Support
For questions or issues, please check the troubleshooting section or create an issue in the project repository.
