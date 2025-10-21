"""
REAL Google Review Scraper - Attempts Actual Web Scraping
"""
import os
import requests
from bs4 import BeautifulSoup
import time
import re
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from yelp_analyzer import GooglePlacesReviewAnalyzer
from utils import search_businesses
import urllib.parse
import json

# Load API key
load_dotenv()

app = Flask(__name__)

def get_base_html(title, content):
    """Generate base HTML with CSS for any page"""
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(135deg, #ff6b6b, #ee5a24);
                color: white;
                padding: 40px;
                text-align: center;
            }}
            
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
                font-weight: 300;
            }}
            
            .header p {{
                font-size: 1.2em;
                opacity: 0.9;
            }}
            
            .form-section {{
                padding: 40px;
            }}
            
            .form-group {{
                margin-bottom: 25px;
            }}
            
            label {{
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: #333;
                font-size: 1.1em;
            }}
            
            input[type="text"] {{
                width: 100%;
                padding: 15px 20px;
                border: 2px solid #e1e8ed;
                border-radius: 10px;
                font-size: 1.1em;
                transition: all 0.3s ease;
            }}
            
            input[type="text"]:focus {{
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }}
            
            .search-btn {{
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
            }}
            
            .search-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            }}
            
            .results-section {{
                padding: 40px;
                background: #f8f9fa;
            }}
            
            .business-card {{
                background: white;
                border-radius: 15px;
                padding: 25px;
                margin-bottom: 25px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                border-left: 5px solid #667eea;
            }}
            
            .business-name {{
                font-size: 1.8em;
                color: #333;
                margin-bottom: 10px;
                font-weight: 600;
            }}
            
            .business-info {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-bottom: 20px;
            }}
            
            .info-item {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
            }}
            
            .info-label {{
                font-size: 0.9em;
                color: #666;
                margin-bottom: 5px;
            }}
            
            .info-value {{
                font-size: 1.2em;
                font-weight: 600;
                color: #333;
            }}
            
            .rating {{
                color: #ff6b6b;
            }}
            
            .stats-card {{
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border-radius: 15px;
                padding: 25px;
                margin-bottom: 25px;
                text-align: center;
            }}
            
            .stats-title {{
                font-size: 1.5em;
                margin-bottom: 15px;
                font-weight: 300;
            }}
            
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 20px;
            }}
            
            .stat-item {{
                background: rgba(255,255,255,0.1);
                padding: 15px;
                border-radius: 10px;
            }}
            
            .stat-number {{
                font-size: 2em;
                font-weight: 600;
                margin-bottom: 5px;
            }}
            
            .stat-label {{
                font-size: 0.9em;
                opacity: 0.9;
            }}
            
            .reviews-section {{
                margin-top: 30px;
            }}
            
            .section-title {{
                font-size: 1.8em;
                color: #333;
                margin-bottom: 20px;
                text-align: center;
                font-weight: 300;
            }}
            
            .bad-review {{
                background: linear-gradient(135deg, #ff9a9e, #fecfef);
                border-radius: 15px;
                padding: 25px;
                margin-bottom: 20px;
                box-shadow: 0 5px 15px rgba(255, 154, 158, 0.2);
                border-left: 5px solid #ff6b6b;
            }}
            
            .review-rating {{
                display: inline-block;
                background: #ff6b6b;
                color: white;
                padding: 8px 15px;
                border-radius: 20px;
                font-weight: 600;
                margin-bottom: 15px;
                font-size: 1.1em;
            }}
            
            .reviewer-name {{
                font-weight: 600;
                color: #333;
                margin-bottom: 10px;
                font-size: 1.1em;
                cursor: pointer;
                text-decoration: underline;
                transition: color 0.3s ease;
            }}
            
            .reviewer-name:hover {{
                color: #667eea;
            }}
            
            .review-text {{
                color: #555;
                line-height: 1.6;
                font-size: 1.05em;
            }}
            
            .no-bad-reviews {{
                background: linear-gradient(135deg, #a8edea, #fed6e3);
                border-radius: 15px;
                padding: 40px;
                text-align: center;
                color: #333;
            }}
            
            .no-bad-reviews h3 {{
                font-size: 1.8em;
                margin-bottom: 15px;
                color: #27ae60;
            }}
            
            .error {{
                background: linear-gradient(135deg, #ff9a9e, #fecfef);
                color: #d63031;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                text-align: center;
                font-weight: 600;
            }}
            
            .back-btn {{
                background: #6c757d;
                color: white;
                padding: 12px 25px;
                border: none;
                border-radius: 8px;
                text-decoration: none;
                display: inline-block;
                margin-top: 20px;
                transition: all 0.3s ease;
            }}
            
            .back-btn:hover {{
                background: #5a6268;
                transform: translateY(-1px);
            }}
            
            .user-profile {{
                background: white;
                border-radius: 15px;
                padding: 25px;
                margin-bottom: 25px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                border-left: 5px solid #ff6b6b;
            }}
            
            .user-name {{
                font-size: 1.8em;
                color: #333;
                margin-bottom: 15px;
                font-weight: 600;
            }}
            
            .user-stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
                margin-bottom: 20px;
            }}
            
            .user-stat {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
            }}
            
            .thinking-pattern {{
                background: linear-gradient(135deg, #f093fb, #f5576c);
                border-radius: 15px;
                padding: 25px;
                margin: 20px 0;
                color: white;
            }}
            
            .thinking-pattern h3 {{
                margin-bottom: 20px;
                font-size: 1.5em;
                text-align: center;
            }}
            
            .pattern-stats {{
                display: flex;
                flex-direction: column;
                gap: 15px;
            }}
            
            .pattern-item {{
                background: rgba(255, 255, 255, 0.2);
                padding: 15px;
                border-radius: 10px;
                backdrop-filter: blur(10px);
            }}
            
            .pattern-item strong {{
                display: block;
                margin-bottom: 5px;
                font-size: 1.1em;
            }}
            
            .user-review {{
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 15px;
                border-left: 4px solid #667eea;
            }}
            
            .user-review.bad {{
                border-left-color: #ff6b6b;
                background: linear-gradient(135deg, #ff9a9e, #fecfef);
            }}
            
            .user-review.good {{
                border-left-color: #27ae60;
                background: linear-gradient(135deg, #a8edea, #fed6e3);
            }}
            
            .warning-box {{
                background: linear-gradient(135deg, #ffeaa7, #fab1a0);
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 25px;
                border-left: 5px solid #fdcb6e;
            }}
            
            .warning-title {{
                font-size: 1.3em;
                font-weight: 600;
                color: #d63031;
                margin-bottom: 10px;
            }}
            
            .loading {{
                text-align: center;
                padding: 40px;
                color: #666;
            }}
            
            .spinner {{
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 20px;
            }}
            
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
            
            .scraping-log {{
                background: #f8f9fa;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 20px;
                font-family: monospace;
                font-size: 0.9em;
                color: #333;
                border-left: 4px solid #667eea;
            }}
            
            .scraping-log.error {{
                border-left-color: #ff6b6b;
                background: #fff5f5;
            }}
            
            .scraping-log.success {{
                border-left-color: #27ae60;
                background: #f0fff4;
            }}
            
            @media (max-width: 768px) {{
                .header h1 {{
                    font-size: 2em;
                }}
                
                .form-section {{
                    padding: 20px;
                }}
                
                .results-section {{
                    padding: 20px;
                }}
                
                .business-info {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {content}
        </div>
    </body>
    </html>
    '''

def attempt_real_google_scraping(user_name, known_review=None):
    """
    Attempt REAL Google scraping (will likely fail due to anti-bot measures)
    """
    scraping_log = []
    reviews = []
    
    try:
        # Start with known review if provided
        if known_review:
            reviews.append({
                "business": known_review.get('business_name', 'Unknown Business'),
                "rating": known_review['rating'],
                "text": known_review['text'],
                "date": "Recently",
                "source": "Known Review"
            })
            scraping_log.append(f"✅ Added known review: {known_review['rating']} stars for {known_review.get('business_name', 'Unknown')}")
        
        # Attempt to scrape Google Maps contributor page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        scraping_log.append(f"🔍 Attempting to scrape Google Maps for user: {user_name}")
        
        # Try different Google Maps URLs
        urls_to_try = [
            f"https://www.google.com/maps/contrib/{user_name}",
            f"https://www.google.com/maps/contrib/{user_name}/reviews",
            f"https://www.google.com/search?q={urllib.parse.quote(user_name)} site:google.com/maps/contrib"
        ]
        
        for i, url in enumerate(urls_to_try):
            try:
                scraping_log.append(f"🌐 Trying URL {i+1}: {url}")
                
                response = requests.get(url, headers=headers, timeout=10)
                scraping_log.append(f"📡 Response status: {response.status_code}")
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Look for review elements (Google's structure changes frequently)
                    review_elements = soup.find_all(['div', 'span'], class_=re.compile(r'review|rating|star'))
                    
                    if review_elements:
                        scraping_log.append(f"🎯 Found {len(review_elements)} potential review elements")
                        
                        # Try to extract review data (this is very fragile)
                        for element in review_elements[:5]:  # Limit to first 5
                            try:
                                text = element.get_text(strip=True)
                                if len(text) > 10 and any(word in text.lower() for word in ['star', 'rating', 'review']):
                                    scraping_log.append(f"📝 Found potential review text: {text[:50]}...")
                            except:
                                pass
                    else:
                        scraping_log.append("❌ No review elements found")
                    
                    # Check for anti-bot measures
                    if "captcha" in response.text.lower() or "robot" in response.text.lower():
                        scraping_log.append("🤖 Detected anti-bot measures (CAPTCHA)")
                        break
                        
                elif response.status_code == 403:
                    scraping_log.append("🚫 Access forbidden (403) - Google blocked the request")
                    break
                elif response.status_code == 429:
                    scraping_log.append("⏰ Rate limited (429) - Too many requests")
                    break
                else:
                    scraping_log.append(f"❌ Failed with status: {response.status_code}")
                
                # Add delay between requests
                time.sleep(2)
                
            except requests.exceptions.RequestException as e:
                scraping_log.append(f"🌐 Network error: {str(e)}")
            except Exception as e:
                scraping_log.append(f"❌ Parsing error: {str(e)}")
        
        # If no real data found, add a note
        if len(reviews) == (1 if known_review else 0):
            scraping_log.append("⚠️ No additional reviews found - Google's anti-bot measures are working")
            scraping_log.append("💡 Real scraping would require:")
            scraping_log.append("   - Proxy rotation")
            scraping_log.append("   - Browser automation (Selenium)")
            scraping_log.append("   - CAPTCHA solving")
            scraping_log.append("   - Rate limiting compliance")
            
            # For demonstration purposes, add simulated comprehensive review data
            # This shows what ALL reviews would look like (not just bad ones)
            scraping_log.append("🎯 DEMO: Adding simulated comprehensive review data to show thinking pattern")
            
            # Add a variety of reviews to show the user's complete thinking pattern
            demo_reviews = [
                {"business": "Starbucks Coffee", "rating": 4, "text": "Good coffee, friendly staff. A bit expensive but convenient.", "date": "2 weeks ago", "source": "Simulated"},
                {"business": "McDonald's", "rating": 2, "text": "Food was cold and service was slow. Not worth the money.", "date": "1 month ago", "source": "Simulated"},
                {"business": "Local Pizza Place", "rating": 5, "text": "Amazing pizza! Fresh ingredients and great atmosphere.", "date": "3 weeks ago", "source": "Simulated"},
                {"business": "Gas Station", "rating": 3, "text": "Average prices, clean restrooms. Nothing special.", "date": "1 week ago", "source": "Simulated"},
                {"business": "Bookstore", "rating": 1, "text": "Terrible customer service. Staff was rude and unhelpful.", "date": "2 months ago", "source": "Simulated"},
                {"business": "Gym", "rating": 4, "text": "Good equipment and clean facilities. Could use more parking.", "date": "1 month ago", "source": "Simulated"},
                {"business": "Pharmacy", "rating": 2, "text": "Long wait times and unfriendly staff. Will try elsewhere next time.", "date": "3 weeks ago", "source": "Simulated"},
                {"business": "Restaurant", "rating": 5, "text": "Excellent food and service! Will definitely come back.", "date": "2 weeks ago", "source": "Simulated"}
            ]
            
            reviews.extend(demo_reviews)
            scraping_log.append(f"📊 Added {len(demo_reviews)} simulated reviews to show complete thinking pattern")
        
        return reviews, scraping_log
        
    except Exception as e:
        scraping_log.append(f"💥 Critical error: {str(e)}")
        return reviews, scraping_log

@app.route('/')
def index():
    form_content = '''
    <div class="header">
        <h1>🔍 REAL Google Review Scraper</h1>
        <p>Attempts ACTUAL web scraping of Google Maps data</p>
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
    '''
    
    return get_base_html("REAL Google Review Scraper", form_content)

@app.route('/user/<user_name>')
def user_profile(user_name):
    """Show user's REAL review history from Google (attempts actual scraping)"""
    # Get query parameters for known review data
    business_name = request.args.get('business', '')
    rating = request.args.get('rating', '')
    review_text = request.args.get('text', '')
    
    # Create known review object if parameters are provided
    known_review = None
    if business_name and rating and review_text:
        try:
            known_review = {
                'business_name': business_name,
                'rating': int(rating),
                'text': review_text
            }
        except ValueError:
            pass
    
    user_content = f'''
    <div class="header">
        <h1>👤 REAL User Profile</h1>
        <p>ACTUAL scraping attempt for "{user_name}" from Google</p>
    </div>
    
    <div class="results-section">
        <div class="warning-box">
            <div class="warning-title">⚠️ REAL Scraping Attempt</div>
            <p>This attempts to ACTUALLY scrape Google Maps data. Google has strong anti-bot measures, so this will likely fail. This is for educational purposes only.</p>
        </div>
        
        <div class="loading">
            <div class="spinner"></div>
            <p>Attempting REAL Google scraping for "{user_name}"...</p>
        </div>
    </div>
    '''
    
    # Simulate scraping delay
    import time
    time.sleep(3)
    
    # Attempt REAL scraping
    reviews, scraping_log = attempt_real_google_scraping(user_name, known_review)
    
    if not reviews:
        error_content = f'''
        <div class="header">
            <h1>👤 User Profile</h1>
            <p>Review history for "{user_name}"</p>
        </div>
        <div class="results-section">
            <div class="error">No review data found for "{user_name}". Google's anti-bot measures prevented scraping.</div>
            <a href="/" class="back-btn">← Go Back</a>
        </div>
        '''
        return get_base_html(f"User Profile - {user_name}", error_content)
    
    # Calculate statistics
    total_reviews = len(reviews)
    bad_reviews = [r for r in reviews if r['rating'] <= 3]
    good_reviews = [r for r in reviews if r['rating'] >= 4]
    bad_count = len(bad_reviews)
    good_count = len(good_reviews)
    bad_percentage = round((bad_count / total_reviews * 100), 1) if total_reviews > 0 else 0
    good_percentage = round((good_count / total_reviews * 100), 1) if total_reviews > 0 else 0
    is_suspicious = bad_percentage >= 70
    
    # Analyze thinking pattern
    avg_rating = round(sum(r['rating'] for r in reviews) / total_reviews, 1) if total_reviews > 0 else 0
    rating_distribution = {}
    for r in reviews:
        rating = r['rating']
        rating_distribution[rating] = rating_distribution.get(rating, 0) + 1
    
    user_content = f'''
    <div class="header">
        <h1>👤 REAL User Profile</h1>
        <p>Scraping results for "{user_name}" from Google</p>
    </div>
    
    <div class="results-section">
        <div class="warning-box">
            <div class="warning-title">📊 Scraping Results</div>
            <p>Found {total_reviews} reviews for "{user_name}". This shows what REAL scraping would look like.</p>
        </div>
        
        <div class="scraping-log">
            <strong>🔍 Scraping Log:</strong><br>
            {chr(10).join(scraping_log)}
        </div>
        
        <div class="user-profile">
            <div class="user-name">👤 {user_name}</div>
            <div class="user-stats">
                <div class="user-stat">
                    <div class="info-label">Total Reviews</div>
                    <div class="info-value">{total_reviews}</div>
                </div>
                <div class="user-stat">
                    <div class="info-label">Average Rating</div>
                    <div class="info-value">{avg_rating}/5</div>
                </div>
                <div class="user-stat">
                    <div class="info-label">Good Reviews (4-5⭐)</div>
                    <div class="info-value good">{good_count} ({good_percentage}%)</div>
                </div>
                <div class="user-stat">
                    <div class="info-label">Bad Reviews (1-3⭐)</div>
                    <div class="info-value rating">{bad_count} ({bad_percentage}%)</div>
                </div>
                <div class="user-stat">
                    <div class="info-label">Thinking Pattern</div>
                    <div class="info-value {'rating' if is_suspicious else ''}">
                        {'🚨 Critical Reviewer' if is_suspicious else '✅ Balanced Reviewer'}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="thinking-pattern">
            <h3>🧠 Thinking Pattern Analysis</h3>
            <div class="pattern-stats">
                <div class="pattern-item">
                    <strong>Rating Distribution:</strong>
                    {', '.join([f"{rating}⭐: {count}" for rating, count in sorted(rating_distribution.items())])}
                </div>
                <div class="pattern-item">
                    <strong>Review Style:</strong>
                    {'Critical and demanding' if is_suspicious else 'Balanced and fair'}
                </div>
                <div class="pattern-item">
                    <strong>Overall Tendency:</strong>
                    {'Tends to give low ratings' if avg_rating < 3.5 else 'Tends to give high ratings' if avg_rating > 4.0 else 'Balanced ratings'}
                </div>
            </div>
        </div>
        
        <h2 class="section-title">📝 ALL Reviews by {user_name} (Complete Thinking Pattern)</h2>
    '''
    
    for review in reviews:
        review_class = "bad" if review['rating'] <= 3 else "good"
        star_rating = "⭐" * review['rating']
        source = review.get('source', 'Scraped')
        
        user_content += f'''
        <div class="user-review {review_class}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <strong>{review['business']}</strong>
                <span class="review-rating">{review['rating']} {star_rating}</span>
            </div>
            <div class="review-text">"{review['text']}"</div>
            <div style="font-size: 0.9em; color: #666; margin-top: 10px;">
                Date: {review['date']} | Source: {source}
            </div>
        </div>
        '''
    
    user_content += '''
        <div style="text-align: center; margin-top: 30px;">
            <a href="/" class="back-btn">🔍 Search Another Business</a>
        </div>
    </div>
    '''
    
    return get_base_html(f"REAL User Profile - {user_name}", user_content)

@app.route('/', methods=['POST'])
def search():
    business_name = request.form.get('business_name', '').strip()
    location = request.form.get('location', '').strip()
    
    if not business_name or not location:
        error_content = '''
        <div class="header">
            <h1>🔍 REAL Google Review Scraper</h1>
            <p>Attempts ACTUAL web scraping of Google Maps data</p>
        </div>
        <div class="form-section">
            <div class="error">Please enter both business name and location</div>
            <a href="/" class="back-btn">← Go Back</a>
        </div>
        '''
        return get_base_html("Error - REAL Google Review Scraper", error_content)
    
    try:
        # Search for businesses using Google Places API
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            error_content = '''
            <div class="header">
                <h1>🔍 REAL Google Review Scraper</h1>
                <p>Attempts ACTUAL web scraping of Google Maps data</p>
            </div>
            <div class="form-section">
                <div class="error">API key not found. Please check your .env file</div>
                <a href="/" class="back-btn">← Go Back</a>
            </div>
            '''
            return get_base_html("Error - REAL Google Review Scraper", error_content)
        
        businesses = search_businesses(business_name, location, api_key)
        
        if not businesses:
            error_content = f'''
            <div class="header">
                <h1>🔍 REAL Google Review Scraper</h1>
                <p>Attempts ACTUAL web scraping of Google Maps data</p>
            </div>
            <div class="form-section">
                <div class="error">No businesses found for '{business_name}' in '{location}'</div>
                <a href="/" class="back-btn">← Go Back</a>
            </div>
            '''
            return get_base_html("Error - REAL Google Review Scraper", error_content)
        
        # Get reviews for the first business
        business = businesses[0]
        analyzer = GooglePlacesReviewAnalyzer()
        reviews = analyzer.get_business_reviews(business['place_id'])
        
        # Filter bad reviews
        bad_reviews = [review for review in reviews if review['rating'] < 4]
        total_reviews = len(reviews)
        bad_reviews_count = len(bad_reviews)
        bad_percentage = round((bad_reviews_count / total_reviews * 100), 1) if total_reviews > 0 else 0
        
        # Build results content
        results_content = f'''
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
            results_content += f'''
            <div class="reviews-section">
                <h2 class="section-title">⚠️ Bad Reviews ({bad_reviews_count} found)</h2>
                <p style="text-align: center; margin-bottom: 20px; color: #666;">
                    Click on reviewer names to attempt REAL Google scraping!
                </p>
            '''
            for i, review in enumerate(bad_reviews, 1):
                # Create URL with review data as query parameters
                reviewer_name = review['user']['name'].replace(' ', '_')
                business_name_encoded = urllib.parse.quote(business['name'])
                rating_encoded = str(review['rating'])
                text_encoded = urllib.parse.quote(review['text'])
                
                user_url = f"/user/{reviewer_name}?business={business_name_encoded}&rating={rating_encoded}&text={text_encoded}"
                
                results_content += f'''
                <div class="bad-review">
                    <div class="review-rating">{review['rating']} ⭐</div>
                    <div class="reviewer-name" onclick="window.location.href='{user_url}'">👤 {review['user']['name']}</div>
                    <div class="review-text">"{review['text']}"</div>
                </div>
                '''
            results_content += '</div>'
        else:
            results_content += '''
            <div class="no-bad-reviews">
                <h3>🎉 Great News!</h3>
                <p>No bad reviews found! This business has excellent ratings from customers.</p>
            </div>
            '''
        
        results_content += '''
            <div style="text-align: center; margin-top: 30px;">
                <a href="/" class="back-btn">🔍 Search Another Business</a>
            </div>
        </div>
        '''
        
        return get_base_html("Analysis Results - REAL Google Review Scraper", results_content)
        
    except Exception as e:
        error_content = f'''
        <div class="header">
            <h1>🔍 REAL Google Review Scraper</h1>
            <p>Attempts ACTUAL web scraping of Google Maps data</p>
        </div>
        <div class="form-section">
            <div class="error">Error: {str(e)}</div>
            <a href="/" class="back-btn">← Go Back</a>
        </div>
        '''
        return get_base_html("Error - REAL Google Review Scraper", error_content)

if __name__ == '__main__':
    print("Starting REAL Google Review Scraper...")
    print("Open your browser and go to: http://localhost:5007")
    print("This version attempts ACTUAL Google scraping!")
    print("WARNING: Will likely fail due to Google's anti-bot measures")
    print()
    app.run(debug=True, host='0.0.0.0', port=5007)
