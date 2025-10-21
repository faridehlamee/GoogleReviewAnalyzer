"""
Simple Business Bad Review Finder
Just run this and enter business name and location
"""
import os
from dotenv import load_dotenv
from yelp_analyzer import GooglePlacesReviewAnalyzer
from utils import search_businesses


def find_bad_reviews_simple():
    """
    Simple function to find bad reviews
    """
    print("BUSINESS BAD REVIEW FINDER")
    print("=" * 40)
    
    # Load API key
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("ERROR: No API key found!")
        return
    
    # Example usage - you can change these
    business_name = "Starbucks"
    location = "New York, NY"
    
    print(f"Searching for bad reviews of '{business_name}' in '{location}'...")
    print()
    
    try:
        # Search for business
        businesses = search_businesses(business_name, location, api_key)
        
        if not businesses:
            print(f"No businesses found for '{business_name}' in '{location}'")
            return
        
        # Use first business found
        business = businesses[0]
        print(f"Found: {business['name']}")
        print(f"Address: {business.get('formatted_address', 'No address')}")
        print(f"Rating: {business.get('rating', 'N/A')} stars")
        print(f"Total Reviews: {business.get('user_ratings_total', 'N/A')}")
        print()
        
        # Get reviews
        analyzer = GooglePlacesReviewAnalyzer()
        reviews = analyzer.get_business_reviews(business['place_id'])
        
        if not reviews:
            print("No reviews found")
            return
        
        # Filter bad reviews
        bad_reviews = [review for review in reviews if review['rating'] < 4]
        
        print(f"Total reviews: {len(reviews)}")
        print(f"Bad reviews (< 4 stars): {len(bad_reviews)}")
        print()
        
        if bad_reviews:
            print("BAD REVIEWS:")
            print("-" * 30)
            
            for i, review in enumerate(bad_reviews, 1):
                print(f"{i}. Rating: {review['rating']} stars")
                print(f"   Reviewer: {review['user']['name']}")
                print(f"   Review: {review['text']}")
                print()
        else:
            print("No bad reviews found!")
            print("This business has good ratings!")
        
    except Exception as e:
        print(f"Error: {e}")


def find_bad_reviews_custom(business_name, location):
    """
    Find bad reviews for custom business
    """
    print(f"Searching for bad reviews of '{business_name}' in '{location}'...")
    
    # Load API key
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("ERROR: No API key found!")
        return
    
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
        print()
        
        # Get reviews
        analyzer = GooglePlacesReviewAnalyzer()
        reviews = analyzer.get_business_reviews(business['place_id'])
        
        if not reviews:
            print("No reviews found")
            return
        
        # Filter bad reviews
        bad_reviews = [review for review in reviews if review['rating'] < 4]
        
        print(f"Bad reviews found: {len(bad_reviews)} out of {len(reviews)} total")
        print()
        
        if bad_reviews:
            for i, review in enumerate(bad_reviews, 1):
                print(f"{i}. {review['rating']} stars - {review['text'][:100]}...")
        else:
            print("No bad reviews found!")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Example 1: Use default business
    find_bad_reviews_simple()
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Custom business
    find_bad_reviews_custom("McDonald's", "Los Angeles, CA")
