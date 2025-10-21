"""
Test Google Places API key with real data
"""
import os
from dotenv import load_dotenv

def test_api_key():
    """
    Test the Google Places API key
    """
    print("TESTING GOOGLE PLACES API KEY")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("No API key found in .env file")
        return False
    
    print(f"API key found: {api_key[:10]}...")
    
    # Test API key with a simple request
    try:
        import requests
        
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': 'Starbucks New York',
            'key': api_key
        }
        
        print("Testing API key with a simple search...")
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'OK':
                print("SUCCESS: API key is working correctly!")
                print(f"Found {len(data.get('results', []))} results")
                
                # Show first result
                if data.get('results'):
                    first_result = data['results'][0]
                    print(f"First result: {first_result.get('name')}")
                    print(f"Place ID: {first_result.get('place_id')}")
                    print(f"Rating: {first_result.get('rating')}")
                
                return True
            else:
                print(f"ERROR: API error: {data.get('error_message', 'Unknown error')}")
                return False
        else:
            print(f"ERROR: HTTP error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    test_api_key()
