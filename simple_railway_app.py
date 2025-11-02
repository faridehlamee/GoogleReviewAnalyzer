"""
Simplified Google Review Analyzer for Railway Deployment
"""
import os
import requests
import json
import urllib.parse
from flask import Flask, request, jsonify
import googlemaps

app = Flask(__name__)

def search_business_and_reviews(business_name, location):
    """Search for a business and get its reviews using Google Places API"""
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        return None, "API key not configured"
    
    # Debug: Check API key format
    if len(api_key) < 20:
        return None, f"API key appears to be invalid (too short: {len(api_key)} characters)"
    
    try:
        # Initialize Google Maps client
        gmaps = googlemaps.Client(key=api_key)
        
        # Search for the business
        search_query = f"{business_name} {location}"
        places_result = gmaps.places(query=search_query)
        
        if not places_result.get('results'):
            return None, f"No businesses found for '{business_name}' in '{location}'"
        
        # Get the first result
        place = places_result['results'][0]
        place_id = place['place_id']
        place_name = place['name']
        place_address = place.get('formatted_address', 'Address not available')
        
        # Get place details including reviews
        place_details = gmaps.place(
            place_id=place_id,
            fields=['name', 'formatted_address', 'rating', 'reviews', 'user_ratings_total']
        )
        
        if 'result' not in place_details:
            return None, "Could not get business details"
        
        result = place_details['result']
        reviews = result.get('reviews', [])
        
        # Filter bad reviews (< 4 stars)
        bad_reviews = [review for review in reviews if review.get('rating', 5) < 4]
        
        return {
            'place_name': place_name,
            'place_address': place_address,
            'place_id': place_id,
            'total_rating': result.get('rating', 'N/A'),
            'total_reviews': result.get('user_ratings_total', 0),
            'all_reviews': reviews,
            'bad_reviews': bad_reviews,
            'bad_reviewers': [review.get('author_name', 'Anonymous') for review in bad_reviews]
        }, None
        
    except Exception as e:
        return None, f"Error searching business: {str(e)}"

def search_businesses_for_leads(search_query, location):
    """Search for multiple businesses (lead finder) using Google Places API"""
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        return None, "API key not configured"
    
    # Debug: Check API key format
    if len(api_key) < 20:
        return None, f"API key appears to be invalid (too short: {len(api_key)} characters)"
    
    try:
        # Initialize Google Maps client
        gmaps = googlemaps.Client(key=api_key)
        
        # Search for businesses
        full_query = f"{search_query} {location}"
        places_result = gmaps.places(query=full_query)
        
        if not places_result.get('results'):
            return None, f"No businesses found for '{search_query}' in '{location}'"
        
        # Get details for each business (up to 20 results)
        leads = []
        for place in places_result['results'][:20]:
            place_id = place.get('place_id')
            place_name = place.get('name', 'Unknown')
            place_address = place.get('formatted_address', 'Address not available')
            rating = place.get('rating', 'N/A')
            total_reviews = place.get('user_ratings_total', 0)
            
            # Get detailed information for each place
            try:
                place_details = gmaps.place(
                    place_id=place_id,
                    fields=['formatted_phone_number', 'website', 'international_phone_number']
                )
                
                if 'result' in place_details:
                    phone = place_details['result'].get('formatted_phone_number', place_details['result'].get('international_phone_number', 'No phone'))
                    website = place_details['result'].get('website', 'No website')
                else:
                    phone = 'No phone'
                    website = 'No website'
                    
            except Exception as e:
                # If we can't get details for one business, continue with others
                phone = 'No phone'
                website = 'No website'
            
            leads.append({
                'name': place_name,
                'address': place_address,
                'phone': phone,
                'website': website,
                'rating': rating,
                'total_reviews': total_reviews
            })
        
        return leads, None
        
    except Exception as e:
        return None, f"Error searching businesses: {str(e)}"

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
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 30px;
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
            
            .form-group label {{
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: #333;
                font-size: 1.1em;
            }}
            
            .form-group input {{
                width: 100%;
                padding: 15px;
                border: 2px solid #e1e5e9;
                border-radius: 10px;
                font-size: 1.1em;
                transition: border-color 0.3s ease;
            }}
            
            .form-group input:focus {{
                outline: none;
                border-color: #667eea;
            }}
            
            .search-btn {{
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 10px;
                font-size: 1.2em;
                cursor: pointer;
                transition: transform 0.3s ease;
                width: 100%;
            }}
            
            .search-btn:hover {{
                transform: translateY(-2px);
            }}
            
            .results-section {{
                padding: 40px;
            }}
            
            .success-box {{
                background: linear-gradient(135deg, #a8edea, #fed6e3);
                border-radius: 15px;
                padding: 25px;
                margin-bottom: 30px;
                text-align: center;
            }}
            
            .success-title {{
                font-size: 1.5em;
                font-weight: 600;
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
                transform: translateY(-2px);
            }}
            
            .tabs {{
                display: flex;
                border-bottom: 2px solid #e1e5e9;
                margin-bottom: 20px;
            }}
            
            .tab {{
                flex: 1;
                padding: 15px;
                text-align: center;
                background: #f8f9fa;
                border: none;
                cursor: pointer;
                font-size: 1.1em;
                font-weight: 600;
                transition: all 0.3s ease;
                color: #667eea;
            }}
            
            .tab:hover {{
                background: #e9ecef;
            }}
            
            .tab.active {{
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border-bottom: 3px solid transparent;
            }}
            
            .tab-content {{
                display: none;
            }}
            
            .tab-content.active {{
                display: block;
            }}
            
            .leads-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                background: white;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                border-radius: 10px;
                overflow: hidden;
            }}
            
            .leads-table th {{
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 15px;
                text-align: left;
                font-weight: 600;
            }}
            
            .leads-table td {{
                padding: 15px;
                border-bottom: 1px solid #e1e5e9;
            }}
            
            .leads-table tr:hover {{
                background: #f8f9fa;
            }}
            
            .leads-table tr:last-child td {{
                border-bottom: none;
            }}
            
            .leads-table a {{
                color: #667eea;
                text-decoration: none;
                word-break: break-all;
            }}
            
            .leads-table a:hover {{
                text-decoration: underline;
            }}
            
            .rating-badge {{
                background: #28a745;
                color: white;
                padding: 5px 10px;
                border-radius: 15px;
                font-weight: 600;
                display: inline-block;
            }}
            
            .table-wrapper {{
                width: 100%;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
                margin-top: 20px;
            }}
            
            .leads-card {{
                display: none;
            }}
            
            @media (max-width: 768px) {{
                body {{
                    padding: 10px;
                }}
                
                .container {{
                    border-radius: 10px;
                }}
                
                .header {{
                    padding: 20px 15px;
                }}
                
                .header h1 {{
                    font-size: 1.8em;
                }}
                
                .form-section {{
                    padding: 20px 15px;
                }}
                
                .results-section {{
                    padding: 20px 15px;
                }}
                
                .form-group input {{
                    font-size: 16px;
                    padding: 12px;
                }}
                
                .leads-table {{
                    display: none;
                }}
                
                .leads-card {{
                    display: block;
                }}
                
                .lead-card {{
                    background: white;
                    border-radius: 10px;
                    padding: 15px;
                    margin-bottom: 15px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                
                .lead-card-header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 10px;
                    padding-bottom: 10px;
                    border-bottom: 2px solid #e1e5e9;
                }}
                
                .lead-card-title {{
                    font-size: 1.2em;
                    font-weight: 600;
                    color: #333;
                    flex: 1;
                }}
                
                .lead-card-number {{
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: 600;
                    margin-right: 10px;
                }}
                
                .lead-card-row {{
                    display: flex;
                    margin-bottom: 10px;
                    padding: 8px 0;
                    border-bottom: 1px solid #f0f0f0;
                }}
                
                .lead-card-label {{
                    font-weight: 600;
                    color: #667eea;
                    min-width: 80px;
                    margin-right: 10px;
                }}
                
                .lead-card-value {{
                    flex: 1;
                    word-break: break-word;
                }}
                
                .lead-card-value a {{
                    color: #667eea;
                    text-decoration: none;
                }}
                
                .lead-card-value a:hover {{
                    text-decoration: underline;
                }}
                
                .tabs {{
                    flex-direction: column;
                }}
                
                .tab {{
                    width: 100%;
                    margin-bottom: 2px;
                }}
            }}
            
            @media (max-width: 480px) {{
                .header h1 {{
                    font-size: 1.5em;
                }}
                
                .header p {{
                    font-size: 1em;
                }}
                
                .lead-card-title {{
                    font-size: 1.1em;
                }}
                
                .lead-card-label {{
                    min-width: 70px;
                    font-size: 0.9em;
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

@app.route('/')
def index():
    """Main search page with tabs for different features"""
    form_content = '''
    <div class="header">
        <h1>🚀 Google Business Tools</h1>
        <p>Review Analysis & Lead Generation</p>
    </div>
    
    <div class="form-section">
        <div class="tabs">
            <button class="tab active" onclick="switchTab('reviews')">📊 Bad Reviews Finder</button>
            <button class="tab" onclick="switchTab('leads')">📋 Lead Generator</button>
        </div>
        
        <!-- Bad Reviews Tab -->
        <div id="reviews-tab" class="tab-content active">
            <form method="POST" action="/">
                <div class="form-group">
                    <label for="business_name">Business Name:</label>
                    <input type="text" id="business_name" name="business_name" placeholder="e.g., McDonald's" required>
                </div>
                
                <div class="form-group">
                    <label for="location">Location:</label>
                    <input type="text" id="location" name="location" placeholder="e.g., Los Angeles, CA" required>
                </div>
                
                <button type="submit" class="search-btn">🔍 Find Bad Reviews</button>
            </form>
        </div>
        
        <!-- Lead Generator Tab -->
        <div id="leads-tab" class="tab-content">
            <form method="POST" action="/lead-finder">
                <div class="form-group">
                    <label for="search_query">Business Type / Category:</label>
                    <input type="text" id="search_query" name="search_query" placeholder="e.g., Financial Advisors" required>
                </div>
                
                <div class="form-group">
                    <label for="lead_location">Location:</label>
                    <input type="text" id="lead_location" name="location" placeholder="e.g., Coquitlam, BC" required>
                </div>
                
                <button type="submit" class="search-btn">🚀 Find Leads</button>
            </form>
        </div>
    </div>
    
    <script>
        function switchTab(tab) {
            // Hide all tab contents
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            // Remove active from all tabs
            document.querySelectorAll('.tab').forEach(t => {
                t.classList.remove('active');
            });
            
            // Show selected tab content and activate tab button
            if (tab === 'reviews') {
                document.getElementById('reviews-tab').classList.add('active');
                document.querySelectorAll('.tab')[0].classList.add('active');
            } else if (tab === 'leads') {
                document.getElementById('leads-tab').classList.add('active');
                document.querySelectorAll('.tab')[1].classList.add('active');
            }
        }
    </script>
    '''
    
    return get_base_html("Google Business Tools", form_content)

@app.route('/', methods=['POST'])
def search_reviews():
    """Search for business reviews and find bad reviewers"""
    business_name = request.form.get('business_name', '').strip()
    location = request.form.get('location', '').strip()
    
    if not business_name or not location:
        error_content = '''
        <div class="header">
            <h1>❌ Error</h1>
            <p>Please provide both business name and location</p>
        </div>
        <div class="results-section">
            <div class="error">Missing required fields</div>
            <a href="/" class="back-btn">← Go Back</a>
        </div>
        '''
        return get_base_html("Error", error_content)
    
    try:
        # Check if API key is available
        api_key = os.environ.get('GOOGLE_API_KEY')
        if not api_key:
            error_content = '''
            <div class="header">
                <h1>❌ Configuration Error</h1>
                <p>Google API key not configured</p>
            </div>
            <div class="results-section">
                <div class="error">Google API key is required but not set in environment variables</div>
                <a href="/" class="back-btn">← Go Back</a>
            </div>
            '''
            return get_base_html("Configuration Error", error_content)
        
        # Search for the actual business and get real reviews
        business_data, error = search_business_and_reviews(business_name, location)
        
        if error:
            error_content = f'''
            <div class="header">
                <h1>❌ Search Error</h1>
                <p>Could not find business or reviews</p>
            </div>
            <div class="results-section">
                <div class="error">{error}</div>
                <a href="/" class="back-btn">← Try Another Search</a>
            </div>
            '''
            return get_base_html("Search Error", error_content)
        
        # Generate results with real data
        bad_reviews_html = ""
        if business_data['bad_reviews']:
            for review in business_data['bad_reviews']:
                reviewer_name = review.get('author_name', 'Anonymous')
                rating = review.get('rating', 'N/A')
                text = review.get('text', 'No review text available')
                time = review.get('time', 'Unknown date')
                
                bad_reviews_html += f'''
                <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #ffc107;">
                    <h4>👤 {reviewer_name}</h4>
                    <p><strong>Rating:</strong> {rating} stars</p>
                    <p><strong>Review:</strong> {text[:200]}{'...' if len(text) > 200 else ''}</p>
                    <p><strong>Date:</strong> {time}</p>
                </div>
                '''
        else:
            bad_reviews_html = '<p style="color: #28a745; font-weight: bold;">🎉 No bad reviews found! This business has good ratings.</p>'
        
        success_content = f'''
        <div class="header">
            <h1>✅ Search Results</h1>
            <p>Found reviews for "{business_data['place_name']}"</p>
        </div>
        
        <div class="results-section">
            <div class="success-box">
                <div class="success-title">🏢 Business Information</div>
                <p><strong>Name:</strong> {business_data['place_name']}</p>
                <p><strong>Address:</strong> {business_data['place_address']}</p>
                <p><strong>Overall Rating:</strong> {business_data['total_rating']} stars</p>
                <p><strong>Total Reviews:</strong> {business_data['total_reviews']}</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h3>📊 Review Analysis:</h3>
                <p><strong>Total Reviews Found:</strong> {len(business_data['all_reviews'])}</p>
                <p><strong>Bad Reviews (< 4 stars):</strong> {len(business_data['bad_reviews'])}</p>
                <p><strong>Bad Reviewers:</strong> {len(business_data['bad_reviewers'])}</p>
            </div>
            
            <div style="background: #e3f2fd; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h3>👥 Bad Reviews ({len(business_data['bad_reviews'])} found):</h3>
                {bad_reviews_html}
            </div>
            
            <a href="/" class="back-btn">← Search Another Business</a>
        </div>
        '''
        
        return get_base_html(f"Results - {business_name}", success_content)
        
    except Exception as e:
        error_content = f'''
        <div class="header">
            <h1>❌ Error</h1>
            <p>An error occurred while searching</p>
        </div>
        <div class="results-section">
            <div class="error">Error: {str(e)}</div>
            <a href="/" class="back-btn">← Go Back</a>
        </div>
        '''
        return get_base_html("Error", error_content)

@app.route('/lead-finder', methods=['POST'])
def lead_finder():
    """Search for multiple businesses and generate a lead list"""
    search_query = request.form.get('search_query', '').strip()
    location = request.form.get('location', '').strip()
    
    if not search_query or not location:
        error_content = '''
        <div class="header">
            <h1>❌ Error</h1>
            <p>Please provide both business type and location</p>
        </div>
        <div class="results-section">
            <div class="error">Missing required fields</div>
            <a href="/" class="back-btn">← Go Back</a>
        </div>
        '''
        return get_base_html("Error", error_content)
    
    try:
        # Check if API key is available
        api_key = os.environ.get('GOOGLE_API_KEY')
        if not api_key:
            error_content = '''
            <div class="header">
                <h1>❌ Configuration Error</h1>
                <p>Google API key not configured</p>
            </div>
            <div class="results-section">
                <div class="error">Google API key is required but not set in environment variables</div>
                <a href="/" class="back-btn">← Go Back</a>
            </div>
            '''
            return get_base_html("Configuration Error", error_content)
        
        # Search for businesses
        leads, error = search_businesses_for_leads(search_query, location)
        
        if error:
            error_content = f'''
            <div class="header">
                <h1>❌ Search Error</h1>
                <p>Could not find businesses</p>
            </div>
            <div class="results-section">
                <div class="error">{error}</div>
                <a href="/" class="back-btn">← Try Another Search</a>
            </div>
            '''
            return get_base_html("Search Error", error_content)
        
        # Generate leads table and mobile cards
        leads_table_html = ""
        leads_cards_html = ""
        if leads:
            # Desktop table view
            leads_table_html = '''
            <div class="table-wrapper">
            <table class="leads-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Business Name</th>
                        <th>Address</th>
                        <th>Phone</th>
                        <th>Website</th>
                        <th>Rating</th>
                        <th>Reviews</th>
                    </tr>
                </thead>
                <tbody>
            '''
            
            # Mobile card view
            leads_cards_html = '<div class="leads-card">'
            
            for idx, lead in enumerate(leads, 1):
                # Format rating badge
                rating_html = '<span class="rating-badge">★ ' + str(lead['rating']) + '</span>' if isinstance(lead['rating'], (int, float)) else 'N/A'
                
                # Format website link
                website_html = f"<a href='{lead['website']}' target='_blank'>Visit Website</a>" if lead['website'] != 'No website' else 'No website'
                
                # Desktop table row
                leads_table_html += f'''
                <tr>
                    <td>{idx}</td>
                    <td><strong>{lead['name']}</strong></td>
                    <td>{lead['address']}</td>
                    <td>{lead['phone']}</td>
                    <td>{website_html}</td>
                    <td>{rating_html}</td>
                    <td>{lead['total_reviews']}</td>
                </tr>
                '''
                
                # Mobile card
                leads_cards_html += f'''
                <div class="lead-card">
                    <div class="lead-card-header">
                        <div style="display: flex; align-items: center; flex: 1;">
                            <div class="lead-card-number">{idx}</div>
                            <div class="lead-card-title">{lead['name']}</div>
                        </div>
                        <div>{rating_html}</div>
                    </div>
                    <div class="lead-card-row">
                        <div class="lead-card-label">📍 Address:</div>
                        <div class="lead-card-value">{lead['address']}</div>
                    </div>
                    <div class="lead-card-row">
                        <div class="lead-card-label">📞 Phone:</div>
                        <div class="lead-card-value">{lead['phone']}</div>
                    </div>
                    <div class="lead-card-row">
                        <div class="lead-card-label">🌐 Website:</div>
                        <div class="lead-card-value">{website_html}</div>
                    </div>
                    <div class="lead-card-row">
                        <div class="lead-card-label">⭐ Reviews:</div>
                        <div class="lead-card-value">{lead['total_reviews']}</div>
                    </div>
                </div>
                '''
            
            leads_table_html += '''
                </tbody>
            </table>
            </div>
            '''
            leads_cards_html += '</div>'
        else:
            leads_table_html = '<p style="color: #28a745; font-weight: bold;">🎉 No leads found for your search criteria.</p>'
            leads_cards_html = '<p style="color: #28a745; font-weight: bold;">🎉 No leads found for your search criteria.</p>'
        
        success_content = f'''
        <div class="header">
            <h1>✅ Lead List Generated</h1>
            <p>Found {len(leads) if leads else 0} businesses for "{search_query}" in "{location}"</p>
        </div>
        
        <div class="results-section">
            <div class="success-box">
                <div class="success-title">📋 Business Leads List</div>
                <p><strong>Search:</strong> {search_query}</p>
                <p><strong>Location:</strong> {location}</p>
                <p><strong>Total Results:</strong> {len(leads) if leads else 0}</p>
            </div>
            
            {leads_table_html}
            {leads_cards_html}
            
            <a href="/" class="back-btn">← Search for More Leads</a>
        </div>
        '''
        
        return get_base_html(f"Leads - {search_query}", success_content)
        
    except Exception as e:
        error_content = f'''
        <div class="header">
            <h1>❌ Error</h1>
            <p>An error occurred while searching for leads</p>
        </div>
        <div class="results-section">
            <div class="error">Error: {str(e)}</div>
            <a href="/" class="back-btn">← Go Back</a>
        </div>
        '''
        return get_base_html("Error", error_content)

@app.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({
        "status": "healthy",
        "message": "Google Review Analyzer is running",
        "api_key_configured": bool(os.environ.get('GOOGLE_API_KEY'))
    })

@app.route('/ping')
def ping():
    """Simple ping endpoint for Railway health checks"""
    return "pong", 200

@app.route('/debug')
def debug():
    """Debug endpoint to check API key status"""
    api_key = os.environ.get('GOOGLE_API_KEY')
    return jsonify({
        "api_key_exists": bool(api_key),
        "api_key_length": len(api_key) if api_key else 0,
        "api_key_preview": api_key[:10] + "..." if api_key and len(api_key) > 10 else "None",
        "api_key_starts_with_AIzaSy": api_key.startswith('AIzaSy') if api_key else False,
        "environment_variables": {k: v for k, v in os.environ.items() if 'GOOGLE' in k or 'API' in k}
    })

@app.route('/test-api')
def test_api():
    """Test if the Google API key actually works"""
    api_key = os.environ.get('GOOGLE_API_KEY')
    
    if not api_key:
        return jsonify({"error": "No API key found"}), 400
    
    if len(api_key) < 30:
        return jsonify({"error": f"API key too short: {len(api_key)} characters"}), 400
    
    if not api_key.startswith('AIzaSy'):
        return jsonify({"error": f"API key doesn't start with 'AIzaSy': {api_key[:10]}"}), 400
    
    try:
        # Test the API key with a simple request
        gmaps = googlemaps.Client(key=api_key)
        result = gmaps.geocode('New York City')
        
        if result:
            return jsonify({
                "success": True,
                "message": "API key works!",
                "test_result": f"Found {len(result)} results for 'New York City'"
            })
        else:
            return jsonify({"error": "API key doesn't work - no results"}), 400
            
    except Exception as e:
        return jsonify({"error": f"API key error: {str(e)}"}), 400

if __name__ == '__main__':
    print("🚂 Starting Google Review Analyzer on Railway...")
    
    # Check if Google API key is set
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY environment variable not set!")
        print("Please set your Google API key in Railway's Variables section")
    else:
        print(f"✅ Google API key found: {api_key[:10]}...")
    
    # Get port from Railway
    port = os.environ.get('PORT', '5008')
    print(f"🌐 Starting server on port {port}")
    print(f"🔍 Health check endpoint: http://0.0.0.0:{port}/ping")
    print(f"🏠 Main page: http://0.0.0.0:{port}/")
    
    try:
        app.run(host='0.0.0.0', port=int(port), debug=False)
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        raise
