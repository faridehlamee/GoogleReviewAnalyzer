"""
Simple Interface for Finding Bad Reviews
Enter a business name and see all bad reviews
"""
import os
from dotenv import load_dotenv
from yelp_analyzer import GooglePlacesReviewAnalyzer
from utils import search_businesses


def find_bad_reviews():
    """
    Simple interface to find bad reviews for a business
    """
    print("BUSINESS BAD REVIEW FINDER")
    print("=" * 50)
    print()
    
    # Load API key
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("ERROR: No API key found!")
        print("Please make sure you have GOOGLE_API_KEY in your .env file")
        return
    
    print("Enter business details to find bad reviews:")
    print()
    
    # Get business name
    business_name = input("Business name: ").strip()
    if not business_name:
        print("Business name is required!")
        return
    
    # Get location
    location = input("Location (city, state): ").strip()
    if not location:
        print("Location is required!")
        return
    
    print()
    print("Searching for business...")
    
    try:
        # Search for business
        businesses = search_businesses(business_name, location, api_key)
        
        if not businesses:
            print(f"No businesses found for '{business_name}' in '{location}'")
            return
        
        # Show search results
        print(f"Found {len(businesses)} businesses:")
        print()
        
        for i, business in enumerate(businesses, 1):
            print(f"{i}. {business['name']}")
            print(f"   Address: {business.get('formatted_address', 'No address')}")
            print(f"   Rating: {business.get('rating', 'N/A')} stars")
            print(f"   Reviews: {business.get('user_ratings_total', 'N/A')} total")
            print()
        
        # Let user select business
        while True:
            try:
                choice = input(f"Select business (1-{len(businesses)}) or 'q' to quit: ").strip()
                if choice.lower() == 'q':
                    return
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(businesses):
                    selected_business = businesses[choice_num - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(businesses)}")
            except ValueError:
                print("Please enter a valid number or 'q' to quit")
        
        # Analyze the selected business
        place_id = selected_business['place_id']
        print()
        print(f"Analyzing reviews for: {selected_business['name']}")
        print("=" * 50)
        
        # Get reviews
        analyzer = GooglePlacesReviewAnalyzer()
        reviews = analyzer.get_business_reviews(place_id)
        
        if not reviews:
            print("No reviews found for this business")
            return
        
        # Filter bad reviews (rating < 4)
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
        
        # Ask if user wants to analyze for suspicious reviewers
        analyze_suspicious = input("Do you want to analyze for suspicious reviewers? (y/n): ").strip().lower()
        
        if analyze_suspicious == 'y':
            print()
            print("Analyzing for suspicious reviewers...")
            print("=" * 50)
            
            results = analyzer.analyze_business_reviews(place_id)
            
            if 'error' not in results:
                print(analyzer.generate_summary_report(results))
            else:
                print(f"Error: {results['error']}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Please check your API key and try again")


def quick_bad_review_search():
    """
    Quick search for bad reviews by business name only
    """
    print("QUICK BAD REVIEW SEARCH")
    print("=" * 30)
    print()
    
    business_name = input("Enter business name: ").strip()
    if not business_name:
        print("Business name is required!")
        return
    
    print(f"Searching for bad reviews of '{business_name}'...")
    
    # Try common locations
    locations = ["New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", "Phoenix, AZ"]
    
    for location in locations:
        try:
            businesses = search_businesses(business_name, location)
            if businesses:
                business = businesses[0]  # Take first result
                place_id = business['place_id']
                
                print(f"Found: {business['name']} in {location}")
                print(f"Rating: {business.get('rating', 'N/A')} stars")
                
                # Get reviews
                analyzer = GooglePlacesReviewAnalyzer()
                reviews = analyzer.get_business_reviews(place_id)
                
                if reviews:
                    bad_reviews = [review for review in reviews if review['rating'] < 4]
                    
                    print(f"Total reviews: {len(reviews)}")
                    print(f"Bad reviews: {len(bad_reviews)}")
                    
                    if bad_reviews:
                        print("\nBAD REVIEWS:")
                        for i, review in enumerate(bad_reviews[:5], 1):  # Show first 5
                            print(f"{i}. {review['rating']} stars - {review['text'][:100]}...")
                    else:
                        print("No bad reviews found!")
                
                return
        
        except Exception as e:
            continue
    
    print(f"No results found for '{business_name}'")


def main():
    """
    Main interface
    """
    print("BUSINESS REVIEW ANALYZER")
    print("=" * 30)
    print()
    print("Choose an option:")
    print("1. Full business search (with location)")
    print("2. Quick search (business name only)")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == '1':
            find_bad_reviews()
            break
        elif choice == '2':
            quick_bad_review_search()
            break
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Please enter 1, 2, or 3")


if __name__ == "__main__":
    main()
