"""
Simple Web Interface for Business Review Analyzer
Run this to get a web interface for finding bad reviews
"""
import os
from flask import Flask, render_template_string, request, jsonify
from dotenv import load_dotenv
from yelp_analyzer import GooglePlacesReviewAnalyzer
from utils import search_businesses

# Load API key
load_dotenv()

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Business Bad Review Finder</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        button { background-color: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background-color: #0056b3; }
        .results { margin-top: 30px; }
        .business { border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; }
        .bad-review { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin-bottom: 10px; border-radius: 5px; }
        .rating { color: #dc3545; font-weight: bold; }
        .error { color: #dc3545; background-color: #f8d7da; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
        .success { color: #155724; background-color: #d4edda; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Business Bad Review Finder</h1>
        <p>Enter a business name and location to find all bad reviews (less than 4 stars)</p>
        
        <form method="POST">
            <div class="form-group">
                <label for="business_name">Business Name:</label>
                <input type="text" id="business_name" name="business_name" placeholder="e.g., Starbucks" required>
            </div>
            
            <div class="form-group">
                <label for="location">Location:</label>
                <input type="text" id="location" name="location" placeholder="e.g., New York, NY" required>
            </div>
            
            <button type="submit">Find Bad Reviews</button>
        </form>
        
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        
        {% if results %}
        <div class="results">
            <h2>Results for "{{ business_name }}" in {{ location }}</h2>
            
            {% if businesses %}
            <h3>Found Businesses:</h3>
            {% for business in businesses %}
            <div class="business">
                <strong>{{ business.name }}</strong><br>
                Address: {{ business.formatted_address }}<br>
                Rating: {{ business.rating }} stars ({{ business.user_ratings_total }} reviews)
            </div>
            {% endfor %}
            {% endif %}
            
            {% if bad_reviews %}
            <h3>Bad Reviews ({{ bad_reviews|length }} found):</h3>
            {% for review in bad_reviews %}
            <div class="bad-review">
                <div class="rating">{{ review.rating }} stars</div>
                <strong>Reviewer:</strong> {{ review.user.name }}<br>
                <strong>Review:</strong> {{ review.text }}
            </div>
            {% endfor %}
            {% else %}
            <div class="success">No bad reviews found! This business has good ratings.</div>
            {% endif %}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        business_name = request.form.get('business_name', '').strip()
        location = request.form.get('location', '').strip()
        
        if not business_name or not location:
            return render_template_string(HTML_TEMPLATE, error="Please enter both business name and location")
        
        try:
            # Search for businesses
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                return render_template_string(HTML_TEMPLATE, error="API key not found. Please check your .env file")
            
            businesses = search_businesses(business_name, location, api_key)
            
            if not businesses:
                return render_template_string(HTML_TEMPLATE, error=f"No businesses found for '{business_name}' in '{location}'")
            
            # Get reviews for the first business
            business = businesses[0]
            analyzer = GooglePlacesReviewAnalyzer()
            reviews = analyzer.get_business_reviews(business['place_id'])
            
            # Filter bad reviews
            bad_reviews = [review for review in reviews if review['rating'] < 4]
            
            return render_template_string(
                HTML_TEMPLATE,
                business_name=business_name,
                location=location,
                businesses=businesses,
                bad_reviews=bad_reviews
            )
            
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, error=f"Error: {str(e)}")
    
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("Starting Business Review Analyzer Web Interface...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
