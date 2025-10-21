"""
Utility functions for Google Places Review Analyzer
"""
import requests
import json
from typing import List, Dict, Optional
from config import GOOGLE_API_KEY


def search_businesses(query: str, location: str, api_key: str = None) -> List[Dict]:
    """
    Search for businesses on Google Places
    
    Args:
        query: Search term (business name, cuisine type, etc.)
        location: Location to search in
        api_key: Google Places API key
        
    Returns:
        List of business dictionaries
    """
    api_key = api_key or GOOGLE_API_KEY
    
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': f"{query} in {location}",
        'key': api_key,
        'fields': 'place_id,name,rating,user_ratings_total,formatted_address'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except requests.exceptions.RequestException as e:
        print(f"Error searching businesses: {e}")
        return []


def get_business_details(place_id: str, api_key: str = None) -> Optional[Dict]:
    """
    Get detailed information about a specific business
    
    Args:
        place_id: Google Places place ID
        api_key: Google Places API key
        
    Returns:
        Business details dictionary or None if error
    """
    api_key = api_key or GOOGLE_API_KEY
    
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'key': api_key,
        'fields': 'place_id,name,rating,user_ratings_total,formatted_address,reviews'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('result', {})
    except requests.exceptions.RequestException as e:
        print(f"Error getting business details: {e}")
        return None


def find_business_id(query: str, location: str, api_key: str = None) -> Optional[str]:
    """
    Find place ID by searching for business name and location
    
    Args:
        query: Business name to search for
        location: Location to search in
        api_key: Google Places API key
        
    Returns:
        Place ID if found, None otherwise
    """
    businesses = search_businesses(query, location, api_key)
    
    if not businesses:
        print(f"No businesses found for '{query}' in '{location}'")
        return None
    
    print(f"Found {len(businesses)} businesses:")
    for i, business in enumerate(businesses, 1):
        print(f"{i}. {business['name']} - {business.get('formatted_address', 'No address')}")
        print(f"   Rating: {business.get('rating', 'N/A')} stars")
        print(f"   Place ID: {business['place_id']}")
        print()
    
    return businesses[0]['place_id'] if businesses else None


def interactive_business_search(api_key: str = None) -> Optional[str]:
    """
    Interactive function to search and select a business
    
    Args:
        api_key: Yelp API key
        
    Returns:
        Selected business ID or None
    """
    print("🔍 Business Search")
    print("=" * 30)
    
    query = input("Enter business name: ").strip()
    if not query:
        print("Business name is required")
        return None
    
    location = input("Enter location (city, state or address): ").strip()
    if not location:
        print("Location is required")
        return None
    
    businesses = search_businesses(query, location, api_key)
    
    if not businesses:
        print(f"No businesses found for '{query}' in '{location}'")
        return None
    
    print(f"\nFound {len(businesses)} businesses:")
    for i, business in enumerate(businesses, 1):
        print(f"{i}. {business['name']}")
        print(f"   Address: {business.get('location', {}).get('address1', 'No address')}")
        print(f"   Rating: {business.get('rating', 'N/A')} stars ({business.get('review_count', 0)} reviews)")
        print(f"   Business ID: {business['id']}")
        print()
    
    while True:
        try:
            choice = input(f"Select business (1-{len(businesses)}) or 'q' to quit: ").strip()
            if choice.lower() == 'q':
                return None
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(businesses):
                selected_business = businesses[choice_num - 1]
                print(f"Selected: {selected_business['name']}")
                return selected_business['place_id']
            else:
                print(f"Please enter a number between 1 and {len(businesses)}")
        except ValueError:
            print("Please enter a valid number or 'q' to quit")


def format_review_summary(review: Dict) -> str:
    """
    Format a review for display
    
    Args:
        review: Review dictionary
        
    Returns:
        Formatted review string
    """
    return f"""
Rating: {review.get('rating', 'N/A')} stars
Reviewer: {review.get('user', {}).get('name', 'Unknown')}
Date: {review.get('time_created', 'Unknown')}
Text: {review.get('text', 'No text')[:200]}...
"""


def export_results_to_csv(results: Dict, filename: str = None):
    """
    Export analysis results to CSV format
    
    Args:
        results: Analysis results dictionary
        filename: Output filename (optional)
    """
    import pandas as pd
    import time
    
    if not filename:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"yelp_analysis_{timestamp}.csv"
    
    # Create DataFrame from results
    data = []
    for user_id, user_data in results.get('user_analysis', {}).items():
        data.append({
            'user_id': user_id,
            'user_name': user_data['name'],
            'total_reviews': user_data['total_reviews'],
            'low_rating_count': user_data['low_rating_count'],
            'low_rating_percentage': user_data['low_rating_percentage'],
            'average_rating': user_data['average_rating'],
            'is_suspicious': user_data['is_suspicious'],
            'target_business_rating': user_data['target_business_rating'],
            'target_business_comment': user_data['target_business_comment'][:100] + "..." if len(user_data['target_business_comment']) > 100 else user_data['target_business_comment']
        })
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Results exported to: {filename}")


if __name__ == "__main__":
    # Example usage
    business_id = interactive_business_search()
    if business_id:
        print(f"Selected business ID: {business_id}")
        print("You can now use this ID with the main analyzer:")
        print(f"python main.py {business_id}")
