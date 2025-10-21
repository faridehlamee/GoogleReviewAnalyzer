"""
Ultra Simple Railway App - Minimal Flask app for Railway deployment
"""
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Google Review Analyzer</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; }
            .success { color: #27ae60; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 Google Review Analyzer</h1>
            <p class="success">✅ Successfully deployed on Railway!</p>
            <p>Your app is now live and working!</p>
            <p><strong>API Key Status:</strong> {'✅ Configured' if os.environ.get('GOOGLE_API_KEY') else '❌ Not Set'}</p>
        </div>
    </body>
    </html>
    '''

@app.route('/ping')
def ping():
    return "pong", 200

@app.route('/health')
def health():
    return {"status": "healthy", "message": "App is running"}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting ultra simple app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
