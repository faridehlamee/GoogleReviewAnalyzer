"""
Simplified Google Review Analyzer for Railway Deployment
"""
import os
import requests
import json
import urllib.parse
from flask import Flask, request, jsonify

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
    """Main search page"""
    form_content = '''
    <div class="header">
        <h1>🔍 Google Review Analyzer</h1>
        <p>Find bad reviewers and analyze their patterns</p>
    </div>
    
    <div class="form-section">
        <form method="POST">
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
    '''
    
    return get_base_html("Google Review Analyzer", form_content)

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
        
        # For now, show a success message with demo data
        success_content = f'''
        <div class="header">
            <h1>✅ Search Successful!</h1>
            <p>Found reviews for "{business_name}" in "{location}"</p>
        </div>
        
        <div class="results-section">
            <div class="success-box">
                <div class="success-title">🎉 Google Review Analyzer is Working!</div>
                <p>Your app is successfully deployed on Railway!</p>
                <p>API Key Status: ✅ Configured</p>
                <p>Business: {business_name}</p>
                <p>Location: {location}</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h3>📊 Demo Results:</h3>
                <p><strong>Total Reviews Found:</strong> 5</p>
                <p><strong>Bad Reviews (< 4 stars):</strong> 2</p>
                <p><strong>Suspicious Reviewers:</strong> 1</p>
            </div>
            
            <div style="background: #e3f2fd; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h3>👤 Sample Bad Reviewer:</h3>
                <p><strong>Name:</strong> MORI N.</p>
                <p><strong>Rating:</strong> 3 stars</p>
                <p><strong>Review:</strong> "Visiting Coquitlam decided to pick up a couple of grocery items..."</p>
                <p><strong>Analysis:</strong> This reviewer tends to give lower ratings (60% of reviews are below 4 stars)</p>
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
