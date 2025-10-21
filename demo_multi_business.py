"""
Demo script showing how to analyze multiple businesses with a single API key
"""
import os
from yelp_analyzer import YelpReviewAnalyzer
from utils import search_businesses, get_business_details


def demo_multiple_businesses():
    """
    Demonstrate analyzing multiple businesses with one API key
    """
    print("DEMO: Analyzing Multiple Businesses with Single API Key")
    print("=" * 60)
    
    # Check if API key is available
    api_key = os.environ.get('YELP_API_KEY')
    if not api_key or api_key == 'your_yelp_api_key_here':
        print("⚠️  No API key found. This demo will use mock data.")
        print("   To use real data, set YELP_API_KEY in your .env file")
        use_mock_data = True
    else:
        print("✅ API key found. Using real Yelp data.")
        use_mock_data = False
    
    # Initialize analyzer
    analyzer = YelpReviewAnalyzer()
    
    if use_mock_data:
        # Demo with mock data
        demo_with_mock_data(analyzer)
    else:
        # Demo with real API
        demo_with_real_api(analyzer)


def demo_with_mock_data(analyzer):
    """
    Demo using mock data (no API key needed)
    """
    print("\n📊 DEMO WITH MOCK DATA")
    print("-" * 30)
    
    # Mock business data
    mock_businesses = [
        {
            'name': 'Demo Restaurant A',
            'id': 'demo_restaurant_a',
            'rating': 4.2,
            'review_count': 150
        },
        {
            'name': 'Demo Restaurant B', 
            'id': 'demo_restaurant_b',
            'rating': 3.8,
            'review_count': 89
        },
        {
            'name': 'Demo Restaurant C',
            'id': 'demo_restaurant_c', 
            'rating': 2.9,
            'review_count': 234
        }
    ]
    
    print(f"Found {len(mock_businesses)} businesses to analyze:")
    for biz in mock_businesses:
        print(f"  - {biz['name']} (Rating: {biz['rating']}, Reviews: {biz['review_count']})")
    
    # Analyze each business
    results_summary = []
    
    for business in mock_businesses:
        print(f"\n🔍 Analyzing {business['name']}...")
        
        # Mock the API calls
        from unittest.mock import patch
        with patch.object(analyzer, 'get_business_reviews') as mock_reviews:
            with patch.object(analyzer, 'get_user_reviews') as mock_user_reviews:
                # Create mock reviews
                mock_reviews.return_value = create_mock_reviews(business['name'])
                mock_user_reviews.return_value = create_mock_user_reviews()
                
                # Run analysis
                results = analyzer.analyze_business_reviews(business['id'])
                
                # Store summary
                results_summary.append({
                    'business_name': business['name'],
                    'total_reviews': results['total_reviews'],
                    'suspicious_users': results['suspicious_users_count']
                })
    
    # Print summary
    print("\n📋 ANALYSIS SUMMARY")
    print("-" * 30)
    for result in results_summary:
        print(f"{result['business_name']}:")
        print(f"  Total Reviews: {result['total_reviews']}")
        print(f"  Suspicious Users: {result['suspicious_users']}")
        print()


def demo_with_real_api(analyzer):
    """
    Demo using real Yelp API
    """
    print("\n📊 DEMO WITH REAL YELP API")
    print("-" * 30)
    
    # Search for businesses
    search_terms = ["Starbucks", "McDonald's", "Pizza Hut"]
    location = "New York, NY"
    
    all_businesses = []
    
    for term in search_terms:
        print(f"🔍 Searching for '{term}' in {location}...")
        businesses = search_businesses(term, location)
        
        if businesses:
            # Take the first result
            business = businesses[0]
            all_businesses.append(business)
            print(f"  Found: {business['name']} (ID: {business['id']})")
        else:
            print(f"  No results found for {term}")
    
    if not all_businesses:
        print("❌ No businesses found. Using mock data instead.")
        demo_with_mock_data(analyzer)
        return
    
    # Analyze each business
    print(f"\n🔍 Analyzing {len(all_businesses)} businesses...")
    
    for business in all_businesses:
        print(f"\n📊 Analyzing {business['name']}...")
        
        try:
            results = analyzer.analyze_business_reviews(business['id'])
            
            if 'error' not in results:
                print(f"✅ Analysis complete:")
                print(f"  Total Reviews: {results['total_reviews']}")
                print(f"  Suspicious Users: {results['suspicious_users_count']}")
            else:
                print(f"❌ Error: {results['error']}")
                
        except Exception as e:
            print(f"❌ Error analyzing {business['name']}: {e}")


def create_mock_reviews(business_name):
    """
    Create mock reviews for demonstration
    """
    return [
        {
            'rating': 5,
            'text': f'Great food at {business_name}!',
            'user': {'id': 'user1', 'name': 'Happy Customer'},
            'time_created': '2023-01-15T10:00:00Z'
        },
        {
            'rating': 2,
            'text': f'Poor service at {business_name}',
            'user': {'id': 'user2', 'name': 'Grumpy Reviewer'},
            'time_created': '2023-01-14T15:30:00Z'
        },
        {
            'rating': 4,
            'text': f'Good experience at {business_name}',
            'user': {'id': 'user3', 'name': 'Satisfied Customer'},
            'time_created': '2023-01-13T20:15:00Z'
        }
    ]


def create_mock_user_reviews():
    """
    Create mock user reviews for demonstration
    """
    return [
        {'rating': 2, 'text': 'Bad service', 'business_id': 'biz1'},
        {'rating': 1, 'text': 'Awful food', 'business_id': 'biz2'},
        {'rating': 2, 'text': 'Poor quality', 'business_id': 'biz3'},
        {'rating': 1, 'text': 'Terrible', 'business_id': 'biz4'},
        {'rating': 2, 'text': 'Disappointing', 'business_id': 'biz5'}
    ]


def main():
    """
    Main demo function
    """
    print("YELP REVIEW ANALYZER - MULTI-BUSINESS DEMO")
    print("=" * 60)
    print()
    print("This demo shows how you can analyze MULTIPLE businesses")
    print("using a SINGLE API key. You don't need separate keys")
    print("for each business you want to analyze!")
    print()
    
    demo_multiple_businesses()
    
    print("\nDEMO COMPLETE!")
    print("=" * 60)
    print()
    print("Key Takeaways:")
    print("✅ ONE API key can analyze ANY business on Yelp")
    print("✅ No need to change keys for different businesses")
    print("✅ Same key works for all your analyses")
    print("✅ Rate limits apply to your total usage, not per business")
    print()
    print("To get your API key:")
    print("1. Go to: https://www.yelp.com/developers/documentation/v3/authentication")
    print("2. Create account and get API key")
    print("3. Add to .env file: YELP_API_KEY=your_key_here")
    print("4. Run: python main.py <business_id>")


if __name__ == "__main__":
    main()
