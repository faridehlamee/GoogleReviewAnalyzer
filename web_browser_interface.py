"""
Web Browser Interface for Business Bad Review Finder
Run this and open your browser to enter any business name and location
"""
import os
from flask import Flask, render_template_string, request, jsonify
from dotenv import load_dotenv
from yelp_analyzer import GooglePlacesReviewAnalyzer
from utils import search_businesses

# Load API key
load_dotenv()

app = Flask(__name__)

# HTML Template with better styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Business Bad Review Finder</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container { 
            max-width: 1000px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .form-group { 
            margin-bottom: 25px; 
        }
        
        label { 
            display: block; 
            margin-bottom: 8px; 
            font-weight: 600;
            color: #333;
            font-size: 1.1em;
        }
        
        input[type="text"] { 
            width: 100%; 
            padding: 15px; 
            border: 2px solid #e1e5e9; 
            border-radius: 8px; 
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        button { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 15px 30px; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            font-size: 18px;
            font-weight: 600;
            transition: transform 0.2s ease;
            width: 100%;
        }
        
        button:hover { 
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .results { 
            margin-top: 40px; 
        }
        
        .business { 
            border: 1px solid #e1e5e9; 
            padding: 20px; 
            margin-bottom: 20px; 
            border-radius: 10px;
            background: #f8f9fa;
            transition: transform 0.2s ease;
        }
        
        .business:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .business h3 {
            color: #333;
            margin-bottom: 10px;
            font-size: 1.3em;
        }
        
        .business-info {
            color: #666;
            margin-bottom: 5px;
        }
        
        .rating {
            font-weight: 600;
            color: #28a745;
        }
        
        .bad-review { 
            background-color: #fff5f5; 
            border: 1px solid #fed7d7; 
            padding: 20px; 
            margin-bottom: 15px; 
            border-radius: 10px;
            border-left: 4px solid #e53e3e;
        }
        
        .bad-review .rating { 
            color: #e53e3e; 
            font-weight: bold; 
            font-size: 1.2em;
            margin-bottom: 10px;
        }
        
        .reviewer {
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
        }
        
        .review-text {
            color: #555;
            line-height: 1.6;
        }
        
        .error { 
            color: #e53e3e; 
            background-color: #fed7d7; 
            padding: 15px; 
            border-radius: 8px; 
            margin-bottom: 20px;
            border-left: 4px solid #e53e3e;
        }
        
        .success { 
            color: #22543d; 
            background-color: #c6f6d5; 
            padding: 15px; 
            border-radius: 8px; 
            margin-bottom: 20px;
            border-left: 4px solid #38a169;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #666;
        }
        
        .stats {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }
        
        .stats h3 {
            color: #333;
            margin-bottom: 10px;
        }
        
        .stats p {
            color: #666;
            margin-bottom: 5px;
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 10px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .content {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Business Bad Review Finder</h1>
            <p>Enter any business name and location to find all bad reviews (less than 4 stars)</p>
            <p><small>Note: Google Places API returns up to 5 reviews per business</small></p>
        </div>
        
        <div class="content">
            <form method="POST">
                <div class="form-group">
                    <label for="business_name">Business Name:</label>
                    <input type="text" id="business_name" name="business_name" 
                           placeholder="e.g., Starbucks, McDonald's, Pizza Hut" required>
                </div>
                
                <div class="form-group">
                    <label for="location">Location:</label>
                    <input type="text" id="location" name="location" 
                           placeholder="e.g., New York, NY or Los Angeles, CA" required>
                </div>
                
                <button type="submit">🔍 Find Bad Reviews</button>
            </form>
            
            {% if error %}
            <div class="error">{{ error }}</div>
            {% endif %}
            
            {% if results %}
            <div class="results">
                <div class="stats">
                    <h3>📊 Analysis Results</h3>
                    <p><strong>Business:</strong> {{ business_name }}</p>
                    <p><strong>Location:</strong> {{ location }}</p>
                    <p><strong>Total Reviews Available:</strong> {{ total_reviews }} (Google Places API limit)</p>
                    <p><strong>Bad Reviews Found:</strong> {{ bad_reviews_count }} ({{ bad_percentage }}%)</p>
                    <p><strong>Note:</strong> Google Places API only returns up to 5 reviews per business</p>
                </div>
                
                {% if businesses %}
                <h3>🏢 Found Businesses:</h3>
                {% for business in businesses %}
                <div class="business">
                    <h3>{{ business.name }}</h3>
                    <div class="business-info">📍 {{ business.formatted_address }}</div>
                    <div class="business-info">⭐ Rating: <span class="rating">{{ business.rating }} stars</span></div>
                    <div class="business-info">📝 Total Reviews: {{ business.user_ratings_total }}</div>
                </div>
                {% endfor %}
                {% endif %}
                
                {% if bad_reviews %}
                <h3>😞 Bad Reviews ({{ bad_reviews|length }} found):</h3>
                {% for review in bad_reviews %}
                <div class="bad-review">
                    <div class="rating">{{ review.rating }} ⭐</div>
                    <div class="reviewer">👤 {{ review.user.name }}</div>
                    <div class="review-text">💬 {{ review.text }}</div>
                </div>
                {% endfor %}
                {% else %}
                <div class="success">
                    <h3>🎉 Great News!</h3>
                    <p>No bad reviews found! This business has good ratings.</p>
                </div>
                {% endif %}
            </div>
            {% endif %}
        </div>
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
            total_reviews = len(reviews)
            bad_reviews_count = len(bad_reviews)
            bad_percentage = round((bad_reviews_count / total_reviews * 100), 1) if total_reviews > 0 else 0
            
            return render_template_string(
                HTML_TEMPLATE,
                business_name=business_name,
                location=location,
                businesses=businesses,
                bad_reviews=bad_reviews,
                total_reviews=total_reviews,
                bad_reviews_count=bad_reviews_count,
                bad_percentage=bad_percentage
            )
            
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, error=f"Error: {str(e)}")
    
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("Starting Business Bad Review Finder Web Interface...")
    print("Open your browser and go to: http://localhost:5000")
    print("Enter any business name and location to find bad reviews!")
    print("Press Ctrl+C to stop the server")
    print()
    app.run(debug=True, host='0.0.0.0', port=5000)
