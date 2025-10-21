"""
Beautiful Web Interface for Business Bad Review Finder
"""
import os
from flask import Flask, request
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
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Business Review Analyzer</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
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
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #ff6b6b, #ee5a24);
                color: white;
                padding: 40px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                font-weight: 300;
            }
            
            .header p {
                font-size: 1.2em;
                opacity: 0.9;
            }
            
            .form-section {
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
                padding: 15px 20px;
                border: 2px solid #e1e8ed;
                border-radius: 10px;
                font-size: 1.1em;
                transition: all 0.3s ease;
            }
            
            input[type="text"]:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            
            .search-btn {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 18px 40px;
                border: none;
                border-radius: 10px;
                font-size: 1.2em;
                font-weight: 600;
                cursor: pointer;
                width: 100%;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .search-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            }
            
            .results-section {
                padding: 40px;
                background: #f8f9fa;
            }
            
            .business-card {
                background: white;
                border-radius: 15px;
                padding: 25px;
                margin-bottom: 25px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                border-left: 5px solid #667eea;
            }
            
            .business-name {
                font-size: 1.8em;
                color: #333;
                margin-bottom: 10px;
                font-weight: 600;
            }
            
            .business-info {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-bottom: 20px;
            }
            
            .info-item {
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
            }
            
            .info-label {
                font-size: 0.9em;
                color: #666;
                margin-bottom: 5px;
            }
            
            .info-value {
                font-size: 1.2em;
                font-weight: 600;
                color: #333;
            }
            
            .rating {
                color: #ff6b6b;
            }
            
            .stats-card {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border-radius: 15px;
                padding: 25px;
                margin-bottom: 25px;
                text-align: center;
            }
            
            .stats-title {
                font-size: 1.5em;
                margin-bottom: 15px;
                font-weight: 300;
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 20px;
            }
            
            .stat-item {
                background: rgba(255,255,255,0.1);
                padding: 15px;
                border-radius: 10px;
            }
            
            .stat-number {
                font-size: 2em;
                font-weight: 600;
                margin-bottom: 5px;
            }
            
            .stat-label {
                font-size: 0.9em;
                opacity: 0.9;
            }
            
            .reviews-section {
                margin-top: 30px;
            }
            
            .section-title {
                font-size: 1.8em;
                color: #333;
                margin-bottom: 20px;
                text-align: center;
                font-weight: 300;
            }
            
            .bad-review {
                background: linear-gradient(135deg, #ff9a9e, #fecfef);
                border-radius: 15px;
                padding: 25px;
                margin-bottom: 20px;
                box-shadow: 0 5px 15px rgba(255, 154, 158, 0.2);
                border-left: 5px solid #ff6b6b;
            }
            
            .review-rating {
                display: inline-block;
                background: #ff6b6b;
                color: white;
                padding: 8px 15px;
                border-radius: 20px;
                font-weight: 600;
                margin-bottom: 15px;
                font-size: 1.1em;
            }
            
            .reviewer-name {
                font-weight: 600;
                color: #333;
                margin-bottom: 10px;
                font-size: 1.1em;
            }
            
            .review-text {
                color: #555;
                line-height: 1.6;
                font-size: 1.05em;
            }
            
            .no-bad-reviews {
                background: linear-gradient(135deg, #a8edea, #fed6e3);
                border-radius: 15px;
                padding: 40px;
                text-align: center;
                color: #333;
            }
            
            .no-bad-reviews h3 {
                font-size: 1.8em;
                margin-bottom: 15px;
                color: #27ae60;
            }
            
            .error {
                background: linear-gradient(135deg, #ff9a9e, #fecfef);
                color: #d63031;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                text-align: center;
                font-weight: 600;
            }
            
            .back-btn {
                background: #6c757d;
                color: white;
                padding: 12px 25px;
                border: none;
                border-radius: 8px;
                text-decoration: none;
                display: inline-block;
                margin-top: 20px;
                transition: all 0.3s ease;
            }
            
            .back-btn:hover {
                background: #5a6268;
                transform: translateY(-1px);
            }
            
            .loading {
                text-align: center;
                padding: 40px;
                color: #666;
            }
            
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 20px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            @media (max-width: 768px) {
                .header h1 {
                    font-size: 2em;
                }
                
                .form-section {
                    padding: 20px;
                }
                
                .results-section {
                    padding: 20px;
                }
                
                .business-info {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔍 Business Review Analyzer</h1>
                <p>Find bad reviews and analyze business reputation</p>
            </div>
            
            <div class="form-section">
                <form method="POST">
                    <div class="form-group">
                        <label for="business_name">Business Name</label>
                        <input type="text" id="business_name" name="business_name" placeholder="e.g., McDonald's, Starbucks, Apple Store" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="location">Location</label>
                        <input type="text" id="location" name="location" placeholder="e.g., Los Angeles, CA or New York, NY" required>
                    </div>
                    
                    <button type="submit" class="search-btn">🔍 Analyze Reviews</button>
                </form>
            </div>
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
            <div class="header">
                <h1>🔍 Business Review Analyzer</h1>
                <p>Find bad reviews and analyze business reputation</p>
            </div>
            <div class="form-section">
                <div class="error">Please enter both business name and location</div>
                <a href="/" class="back-btn">← Go Back</a>
            </div>
        </div>
        '''
    
    try:
        # Search for businesses
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            return f'''
            <div class="container">
                <div class="header">
                    <h1>🔍 Business Review Analyzer</h1>
                    <p>Find bad reviews and analyze business reputation</p>
                </div>
                <div class="form-section">
                    <div class="error">API key not found. Please check your .env file</div>
                    <a href="/" class="back-btn">← Go Back</a>
                </div>
            </div>
            '''
        
        businesses = search_businesses(business_name, location, api_key)
        
        if not businesses:
            return f'''
            <div class="container">
                <div class="header">
                    <h1>🔍 Business Review Analyzer</h1>
                    <p>Find bad reviews and analyze business reputation</p>
                </div>
                <div class="form-section">
                    <div class="error">No businesses found for '{business_name}' in '{location}'</div>
                    <a href="/" class="back-btn">← Go Back</a>
                </div>
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
        bad_percentage = round((bad_reviews_count / total_reviews * 100), 1) if total_reviews > 0 else 0
        
        # Build results HTML
        results_html = f'''
        <div class="container">
            <div class="header">
                <h1>📊 Analysis Results</h1>
                <p>Review analysis for "{business_name}" in {location}</p>
            </div>
            
            <div class="results-section">
                <div class="business-card">
                    <div class="business-name">{business['name']}</div>
                    <div class="business-info">
                        <div class="info-item">
                            <div class="info-label">Address</div>
                            <div class="info-value">{business.get('formatted_address', 'No address available')}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Overall Rating</div>
                            <div class="info-value rating">{business.get('rating', 'N/A')} ⭐</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Total Reviews</div>
                            <div class="info-value">{business.get('user_ratings_total', 'N/A')}</div>
                        </div>
                    </div>
                </div>
                
                <div class="stats-card">
                    <div class="stats-title">📈 Review Analysis</div>
                    <div class="stats-grid">
                        <div class="stat-item">
                            <div class="stat-number">{total_reviews}</div>
                            <div class="stat-label">Reviews Analyzed</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">{bad_reviews_count}</div>
                            <div class="stat-label">Bad Reviews</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">{bad_percentage}%</div>
                            <div class="stat-label">Bad Review Rate</div>
                        </div>
                    </div>
                </div>
        '''
        
        if bad_reviews:
            results_html += f'''
                <div class="reviews-section">
                    <h2 class="section-title">⚠️ Bad Reviews ({bad_reviews_count} found)</h2>
            '''
            for i, review in enumerate(bad_reviews, 1):
                results_html += f'''
                    <div class="bad-review">
                        <div class="review-rating">{review['rating']} ⭐</div>
                        <div class="reviewer-name">👤 {review['user']['name']}</div>
                        <div class="review-text">"{review['text']}"</div>
                    </div>
                '''
            results_html += '</div>'
        else:
            results_html += '''
                <div class="no-bad-reviews">
                    <h3>🎉 Great News!</h3>
                    <p>No bad reviews found! This business has excellent ratings from customers.</p>
                </div>
            '''
        
        results_html += '''
                <div style="text-align: center; margin-top: 30px;">
                    <a href="/" class="back-btn">🔍 Search Another Business</a>
                </div>
            </div>
        </div>
        '''
        
        return results_html
        
    except Exception as e:
        return f'''
        <div class="container">
            <div class="header">
                <h1>🔍 Business Review Analyzer</h1>
                <p>Find bad reviews and analyze business reputation</p>
            </div>
            <div class="form-section">
                <div class="error">Error: {str(e)}</div>
                <a href="/" class="back-btn">← Go Back</a>
            </div>
        </div>
        '''

if __name__ == '__main__':
    print("Starting Beautiful Web Interface...")
    print("Open your browser and go to: http://localhost:5003")
    print("This version has a beautiful, modern design!")
    print()
    app.run(debug=True, host='0.0.0.0', port=5003)
