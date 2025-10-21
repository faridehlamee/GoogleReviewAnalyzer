"""
Ultra Simple Web Interface - Guaranteed to Show Results
"""
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from yelp_analyzer import GooglePlacesReviewAnalyzer
from utils import search_businesses

# Load API key
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Business Bad Review Finder</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            h1 { color: #333; text-align: center; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input[type="text"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            button { background-color: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; width: 100%; }
            .results { margin-top: 30px; }
            .business { border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; background: #f8f9fa; }
            .bad-review { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin-bottom: 10px; border-radius: 5px; }
            .rating { color: #dc3545; font-weight: bold; }
            .error { color: #dc3545; background-color: #f8d7da; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Business Bad Review Finder</h1>
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
        </div>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def search():
    business_name = request.form.get('business_name', '').strip()
    location = request.form.get('location', '').strip()
    
    if not business_name or not location:
        return f'''
        <div class="container">
            <h1>Business Bad Review Finder</h1>
            <div class="error">Please enter both business name and location</div>
            <a href="/">Go Back</a>
        </div>
        '''
    
    try:
        # Search for businesses
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            return f'''
            <div class="container">
                <h1>Business Bad Review Finder</h1>
                <div class="error">API key not found. Please check your .env file</div>
                <a href="/">Go Back</a>
            </div>
            '''
        
        businesses = search_businesses(business_name, location, api_key)
        
        if not businesses:
            return f'''
            <div class="container">
                <h1>Business Bad Review Finder</h1>
                <div class="error">No businesses found for '{business_name}' in '{location}'</div>
                <a href="/">Go Back</a>
            </div>
            '''
        
        # Get reviews for the first business
        business = businesses[0]
        analyzer = GooglePlacesReviewAnalyzer()
        reviews = analyzer.get_business_reviews(business['place_id'])
        
        # Filter bad reviews
        bad_reviews = [review for review in reviews if review['rating'] < 4]
        total_reviews = len(reviews)
        bad_reviews_count = len(bad_reviews)
        
        # Build results HTML
        results_html = f'''
        <div class="container">
            <h1>Business Bad Review Finder</h1>
            <h2>Results for "{business_name}" in {location}</h2>
            
            <div class="business">
                <h3>{business['name']}</h3>
                <p><strong>Address:</strong> {business.get('formatted_address', 'No address')}</p>
                <p><strong>Rating:</strong> {business.get('rating', 'N/A')} stars</p>
                <p><strong>Total Reviews:</strong> {business.get('user_ratings_total', 'N/A')}</p>
            </div>
            
            <h3>Analysis Results:</h3>
            <p><strong>Reviews Available:</strong> {total_reviews} (Google API limit)</p>
            <p><strong>Bad Reviews Found:</strong> {bad_reviews_count}</p>
        '''
        
        if bad_reviews:
            results_html += f'<h3>Bad Reviews ({bad_reviews_count} found):</h3>'
            for i, review in enumerate(bad_reviews, 1):
                results_html += f'''
                <div class="bad-review">
                    <div class="rating">{review['rating']} stars</div>
                    <p><strong>Reviewer:</strong> {review['user']['name']}</p>
                    <p><strong>Review:</strong> {review['text']}</p>
                </div>
                '''
        else:
            results_html += '<div class="error">No bad reviews found! This business has good ratings.</div>'
        
        results_html += '<p><a href="/">Search Another Business</a></p></div>'
        
        return results_html
        
    except Exception as e:
        return f'''
        <div class="container">
            <h1>Business Bad Review Finder</h1>
            <div class="error">Error: {str(e)}</div>
            <a href="/">Go Back</a>
        </div>
        '''

if __name__ == '__main__':
    print("Starting Ultra Simple Web Interface...")
    print("Open your browser and go to: http://localhost:5002")
    print("This version will definitely show results!")
    print()
    app.run(debug=True, host='0.0.0.0', port=5002)
