"""
Debug version to see what's happening with the web interface
"""
import os
from flask import Flask, render_template_string, request
from dotenv import load_dotenv
from yelp_analyzer import GooglePlacesReviewAnalyzer
from utils import search_businesses

# Load API key
load_dotenv()

app = Flask(__name__)

# Simple HTML Template with debug info
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Business Bad Review Finder - Debug</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        button { background-color: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; width: 100%; }
        button:hover { background-color: #0056b3; }
        .results { margin-top: 30px; }
        .business { border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; background: #f8f9fa; }
        .bad-review { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin-bottom: 10px; border-radius: 5px; }
        .rating { color: #dc3545; font-weight: bold; }
        .error { color: #dc3545; background-color: #f8d7da; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
        .success { color: #155724; background-color: #d4edda; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
        .stats { background: #e9ecef; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .debug { background: #f8f9fa; padding: 10px; border-radius: 5px; margin-bottom: 20px; font-family: monospace; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Business Bad Review Finder - Debug Version</h1>
        <p>Enter any business name and location to find bad reviews (less than 4 stars)</p>
        
        <form method="POST">
            <div class="form-group">
                <label for="business_name">Business Name:</label>
                <input type="text" id="business_name" name="business_name" placeholder="e.g., McDonald's" required>
            </div>
            
            <div class="form-group">
                <label for="location">Location:</label>
                <input type="text" id="location" name="location" placeholder="e.g., Los Angeles, CA" required>
            </div>
            
            <button type="submit">Find Bad Reviews</button>
        </form>
        
        {% if debug_info %}
        <div class="debug">
            <strong>Debug Info:</strong><br>
            {{ debug_info }}
        </div>
        {% endif %}
        
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        
        {% if results %}
        <div class="results">
            <div class="stats">
                <h3>Analysis Results</h3>
                <p><strong>Business:</strong> {{ business_name }}</p>
                <p><strong>Location:</strong> {{ location }}</p>
                <p><strong>Reviews Available:</strong> {{ total_reviews }} (Google API limit)</p>
                <p><strong>Bad Reviews:</strong> {{ bad_reviews_count }} ({{ bad_percentage }}%)</p>
            </div>
            
            {% if businesses %}
            <h3>Found Businesses:</h3>
            {% for business in businesses %}
            <div class="business">
                <strong>{{ business.name }}</strong><br>
                Address: {{ business.formatted_address }}<br>
                Rating: {{ business.rating }} stars ({{ business.user_ratings_total }} total reviews)
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
    debug_info = ""
    
    if request.method == 'POST':
        business_name = request.form.get('business_name', '').strip()
        location = request.form.get('location', '').strip()
        
        debug_info += f"POST request received. Business: '{business_name}', Location: '{location}'<br>"
        
        if not business_name or not location:
            debug_info += "Error: Missing business name or location<br>"
            return render_template_string(HTML_TEMPLATE, error="Please enter both business name and location", debug_info=debug_info)
        
        try:
            # Search for businesses
            api_key = os.getenv('GOOGLE_API_KEY')
            debug_info += f"API key found: {api_key[:10] if api_key else 'None'}...<br>"
            
            if not api_key:
                debug_info += "Error: No API key found<br>"
                return render_template_string(HTML_TEMPLATE, error="API key not found. Please check your .env file", debug_info=debug_info)
            
            debug_info += f"Searching for businesses...<br>"
            businesses = search_businesses(business_name, location, api_key)
            debug_info += f"Found {len(businesses) if businesses else 0} businesses<br>"
            
            if not businesses:
                debug_info += "Error: No businesses found<br>"
                return render_template_string(HTML_TEMPLATE, error=f"No businesses found for '{business_name}' in '{location}'", debug_info=debug_info)
            
            # Get reviews for the first business
            business = businesses[0]
            debug_info += f"Using business: {business['name']}<br>"
            debug_info += f"Place ID: {business['place_id']}<br>"
            
            analyzer = GooglePlacesReviewAnalyzer()
            debug_info += "Getting reviews...<br>"
            reviews = analyzer.get_business_reviews(business['place_id'])
            debug_info += f"Got {len(reviews) if reviews else 0} reviews<br>"
            
            if reviews:
                debug_info += "Reviews: " + str([r['rating'] for r in reviews]) + "<br>"
            
            # Filter bad reviews
            bad_reviews = [review for review in reviews if review['rating'] < 4]
            total_reviews = len(reviews)
            bad_reviews_count = len(bad_reviews)
            bad_percentage = round((bad_reviews_count / total_reviews * 100), 1) if total_reviews > 0 else 0
            
            debug_info += f"Bad reviews: {bad_reviews_count} out of {total_reviews}<br>"
            
            return render_template_string(
                HTML_TEMPLATE,
                business_name=business_name,
                location=location,
                businesses=businesses,
                bad_reviews=bad_reviews,
                total_reviews=total_reviews,
                bad_reviews_count=bad_reviews_count,
                bad_percentage=bad_percentage,
                debug_info=debug_info
            )
            
        except Exception as e:
            debug_info += f"Exception: {str(e)}<br>"
            import traceback
            debug_info += traceback.format_exc().replace('\n', '<br>')
            return render_template_string(HTML_TEMPLATE, error=f"Error: {str(e)}", debug_info=debug_info)
    
    return render_template_string(HTML_TEMPLATE, debug_info=debug_info)

if __name__ == '__main__':
    print("Starting Debug Web Interface...")
    print("Open your browser and go to: http://localhost:5001")
    print("This will show debug information to help identify the issue")
    print()
    app.run(debug=True, host='0.0.0.0', port=5001)
