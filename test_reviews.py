"""
Test to see what reviews we're getting from Google Places API
"""
import os
from dotenv import load_dotenv
from yelp_analyzer import GooglePlacesReviewAnalyzer
from utils import search_businesses


def test_reviews():
    """
    Test what reviews we're getting
    """
    print("TESTING GOOGLE PLACES REVIEWS")
    print("=" * 40)
    
    # Load API key
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("ERROR: No API key found!")
        return
    
    # Test with a business
    business_name = "McDonald's"
    location = "Los Angeles, CA"
    
    print(f"Searching for '{business_name}' in '{location}'...")
    
    try:
        # Search for business
        businesses = search_businesses(business_name, location, api_key)
        
        if not businesses:
            print(f"No businesses found for '{business_name}' in '{location}'")
            return
        
        # Use first business found
        business = businesses[0]
        print(f"Found: {business['name']}")
        print(f"Rating: {business.get('rating', 'N/A')} stars")
        print(f"Total Reviews: {business.get('user_ratings_total', 'N/A')}")
        print()
        
        # Get reviews
        analyzer = GooglePlacesReviewAnalyzer()
        reviews = analyzer.get_business_reviews(business['place_id'])
        
        print(f"Reviews returned by API: {len(reviews)}")
        print()
        
        if reviews:
            print("ALL REVIEWS:")
            print("-" * 30)
            
            for i, review in enumerate(reviews, 1):
                print(f"{i}. Rating: {review['rating']} stars")
                print(f"   Reviewer: {review['user']['name']}")
                print(f"   Text: {review['text'][:100]}...")
                print()
            
            # Filter bad reviews
            bad_reviews = [review for review in reviews if review['rating'] < 4]
            
            print(f"BAD REVIEWS (< 4 stars): {len(bad_reviews)}")
            print("-" * 30)
            
            if bad_reviews:
                for i, review in enumerate(bad_reviews, 1):
                    print(f"{i}. Rating: {review['rating']} stars")
                    print(f"   Reviewer: {review['user']['name']}")
                    print(f"   Text: {review['text']}")
                    print()
            else:
                print("No bad reviews found in the returned reviews")
        else:
            print("No reviews returned by the API")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_reviews()
