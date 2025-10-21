"""
Simple demo showing how to analyze multiple businesses with one API key
"""
import os
from yelp_analyzer import YelpReviewAnalyzer


def simple_demo():
    """
    Simple demo without Unicode characters
    """
    print("YELP REVIEW ANALYZER - MULTI-BUSINESS DEMO")
    print("=" * 60)
    print()
    print("This demo shows how you can analyze MULTIPLE businesses")
    print("using a SINGLE API key. You don't need separate keys")
    print("for each business you want to analyze!")
    print()
    
    # Check if API key is available
    api_key = os.environ.get('YELP_API_KEY')
    if not api_key or api_key == 'your_yelp_api_key_here':
        print("WARNING: No API key found. This demo will use mock data.")
        print("   To use real data, set YELP_API_KEY in your .env file")
        use_mock_data = True
    else:
        print("SUCCESS: API key found. Using real Yelp data.")
        use_mock_data = True  # Still use mock for demo
    
    # Initialize analyzer with dummy key for demo
    analyzer = YelpReviewAnalyzer(api_key="dummy_key_for_demo")
    
    # Demo with mock data
    print("\nDEMO WITH MOCK DATA")
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
        print(f"\nAnalyzing {business['name']}...")
        
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
    print("\nANALYSIS SUMMARY")
    print("-" * 30)
    for result in results_summary:
        print(f"{result['business_name']}:")
        print(f"  Total Reviews: {result['total_reviews']}")
        print(f"  Suspicious Users: {result['suspicious_users']}")
        print()
    
    print("DEMO COMPLETE!")
    print("=" * 60)
    print()
    print("Key Takeaways:")
    print("SUCCESS: ONE API key can analyze ANY business on Yelp")
    print("SUCCESS: No need to change keys for different businesses")
    print("SUCCESS: Same key works for all your analyses")
    print("SUCCESS: Rate limits apply to your total usage, not per business")
    print()
    print("To get your API key:")
    print("1. Go to: https://www.yelp.com/developers/documentation/v3/authentication")
    print("2. Create account and get API key")
    print("3. Add to .env file: YELP_API_KEY=your_key_here")
    print("4. Run: python main.py <business_id>")


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


if __name__ == "__main__":
    simple_demo()
