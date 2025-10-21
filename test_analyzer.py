"""
Test script for Yelp Review Analyzer
This script helps you test the analyzer with different scenarios
"""
import os
import sys
import json
from unittest.mock import patch, MagicMock
from yelp_analyzer import YelpReviewAnalyzer
from visualizer import YelpDataVisualizer
from utils import search_businesses, get_business_details


def test_without_api_key():
    """
    Test 1: Test analyzer initialization without API key
    """
    print("=" * 60)
    print("TEST 1: Testing without API key")
    print("=" * 60)
    
    try:
        # Temporarily remove API key
        original_key = os.environ.get('YELP_API_KEY')
        if 'YELP_API_KEY' in os.environ:
            del os.environ['YELP_API_KEY']
        
        analyzer = YelpReviewAnalyzer(api_key=None)
        print("❌ ERROR: Should have failed without API key")
        return False
        
    except ValueError as e:
        print(f"✅ SUCCESS: Correctly failed with error: {e}")
        return True
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        return False
    finally:
        # Restore API key
        if original_key:
            os.environ['YELP_API_KEY'] = original_key


def test_with_mock_data():
    """
    Test 2: Test analyzer with mock data
    """
    print("=" * 60)
    print("TEST 2: Testing with mock data")
    print("=" * 60)
    
    # Create mock reviews data
    mock_reviews = [
        {
            'rating': 5,
            'text': 'Great food and service!',
            'user': {'id': 'user1', 'name': 'Happy Customer'},
            'time_created': '2023-01-15T10:00:00Z'
        },
        {
            'rating': 2,
            'text': 'Terrible experience, avoid this place.',
            'user': {'id': 'user2', 'name': 'Grumpy Reviewer'},
            'time_created': '2023-01-14T15:30:00Z'
        },
        {
            'rating': 1,
            'text': 'Worst restaurant ever!',
            'user': {'id': 'user3', 'name': 'Negative Nancy'},
            'time_created': '2023-01-13T20:15:00Z'
        },
        {
            'rating': 4,
            'text': 'Good food, nice atmosphere.',
            'user': {'id': 'user4', 'name': 'Satisfied Customer'},
            'time_created': '2023-01-12T12:00:00Z'
        },
        {
            'rating': 3,
            'text': 'Average experience, nothing special.',
            'user': {'id': 'user5', 'name': 'Neutral Reviewer'},
            'time_created': '2023-01-11T18:45:00Z'
        }
    ]
    
    # Create analyzer with dummy API key
    analyzer = YelpReviewAnalyzer(api_key="dummy_key_for_testing")
    
    # Mock the API call to return our test data
    with patch.object(analyzer, 'get_business_reviews', return_value=mock_reviews):
        with patch.object(analyzer, 'get_user_reviews') as mock_user_reviews:
            # Mock user review data for the low-rating users
            mock_user_reviews.side_effect = [
                # User 2 (Grumpy Reviewer) - mostly negative reviews
                [
                    {'rating': 2, 'text': 'Bad service', 'business_id': 'biz1'},
                    {'rating': 1, 'text': 'Awful food', 'business_id': 'biz2'},
                    {'rating': 2, 'text': 'Poor quality', 'business_id': 'biz3'},
                    {'rating': 1, 'text': 'Terrible', 'business_id': 'biz4'},
                    {'rating': 2, 'text': 'Disappointing', 'business_id': 'biz5'},
                    {'rating': 1, 'text': 'Worst ever', 'business_id': 'biz6'},
                    {'rating': 2, 'text': 'Not recommended', 'business_id': 'biz7'},
                    {'rating': 1, 'text': 'Horrible', 'business_id': 'biz8'}
                ],
                # User 3 (Negative Nancy) - mostly negative reviews
                [
                    {'rating': 1, 'text': 'Terrible', 'business_id': 'biz9'},
                    {'rating': 2, 'text': 'Bad', 'business_id': 'biz10'},
                    {'rating': 1, 'text': 'Awful', 'business_id': 'biz11'},
                    {'rating': 1, 'text': 'Horrible', 'business_id': 'biz12'},
                    {'rating': 2, 'text': 'Poor', 'business_id': 'biz13'},
                    {'rating': 1, 'text': 'Worst', 'business_id': 'biz14'},
                    {'rating': 2, 'text': 'Disappointing', 'business_id': 'biz15'},
                    {'rating': 1, 'text': 'Bad service', 'business_id': 'biz16'},
                    {'rating': 1, 'text': 'Terrible food', 'business_id': 'biz17'},
                    {'rating': 2, 'text': 'Not good', 'business_id': 'biz18'}
                ]
            ]
            
            # Run the analysis
            results = analyzer.analyze_business_reviews("test_business_id")
            
            # Check results
            print(f"Total reviews analyzed: {results['total_reviews']}")
            print(f"Low rating reviews: {results['low_rating_reviews']}")
            print(f"Suspicious users found: {results['suspicious_users_count']}")
            
            # Print detailed results
            for user_id, user_data in results['user_analysis'].items():
                print(f"\nUser: {user_data['name']}")
                print(f"  Total reviews: {user_data['total_reviews']}")
                print(f"  Low rating percentage: {user_data['low_rating_percentage']:.1%}")
                print(f"  Average rating: {user_data['average_rating']:.1f}")
                print(f"  Is suspicious: {user_data['is_suspicious']}")
            
            print("\n" + analyzer.generate_summary_report(results))
            
            return True


def test_business_search():
    """
    Test 3: Test business search functionality
    """
    print("=" * 60)
    print("TEST 3: Testing business search")
    print("=" * 60)
    
    # Test with mock data
    mock_businesses = [
        {
            'id': 'test_biz_1',
            'name': 'Test Restaurant',
            'rating': 4.5,
            'review_count': 150,
            'location': {'address1': '123 Test St', 'city': 'Test City'}
        },
        {
            'id': 'test_biz_2', 
            'name': 'Another Test Place',
            'rating': 3.8,
            'review_count': 75,
            'location': {'address1': '456 Test Ave', 'city': 'Test City'}
        }
    ]
    
    with patch('utils.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {'businesses': mock_businesses}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        businesses = search_businesses("test restaurant", "test city", "dummy_key")
        
        if businesses:
            print(f"✅ SUCCESS: Found {len(businesses)} businesses")
            for biz in businesses:
                print(f"  - {biz['name']} (ID: {biz['id']})")
            return True
        else:
            print("❌ ERROR: No businesses found")
            return False


def test_visualizer():
    """
    Test 4: Test visualization functionality
    """
    print("=" * 60)
    print("TEST 4: Testing visualizer")
    print("=" * 60)
    
    # Create test data
    test_results = {
        'business_id': 'test_business',
        'total_reviews': 10,
        'low_rating_reviews': 3,
        'suspicious_users_count': 1,
        'user_analysis': {
            'user1': {
                'name': 'Test User',
                'total_reviews': 8,
                'low_rating_count': 6,
                'low_rating_percentage': 0.75,
                'average_rating': 2.5,
                'is_suspicious': True,
                'target_business_rating': 2,
                'target_business_comment': 'Not good'
            }
        },
        'suspicious_users': ['user1'],
        'all_reviews': [
            {'rating': 5, 'text': 'Great!'},
            {'rating': 4, 'text': 'Good'},
            {'rating': 3, 'text': 'Average'},
            {'rating': 2, 'text': 'Not great'},
            {'rating': 1, 'text': 'Terrible'}
        ]
    }
    
    try:
        visualizer = YelpDataVisualizer(output_dir='test_output')
        
        # Test plotting functions
        visualizer.plot_rating_distribution(test_results, save=False)
        print("✅ Rating distribution plot created successfully")
        
        visualizer.plot_suspicious_users_analysis(test_results, save=False)
        print("✅ Suspicious users analysis plot created successfully")
        
        visualizer.create_summary_dashboard(test_results, save=False)
        print("✅ Summary dashboard created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR in visualizer test: {e}")
        return False


def test_config_loading():
    """
    Test 5: Test configuration loading
    """
    print("=" * 60)
    print("TEST 5: Testing configuration loading")
    print("=" * 60)
    
    try:
        from config import LOW_RATING_THRESHOLD, SUSPICIOUS_THRESHOLD, MIN_REVIEWS_FOR_ANALYSIS
        
        print(f"✅ Configuration loaded successfully:")
        print(f"  - Low rating threshold: {LOW_RATING_THRESHOLD}")
        print(f"  - Suspicious threshold: {SUSPICIOUS_THRESHOLD}")
        print(f"  - Min reviews for analysis: {MIN_REVIEWS_FOR_ANALYSIS}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR loading configuration: {e}")
        return False


def run_integration_test():
    """
    Integration test with real API (if API key is available)
    """
    print("=" * 60)
    print("INTEGRATION TEST: Testing with real API")
    print("=" * 60)
    
    # Check if API key is available
    api_key = os.environ.get('YELP_API_KEY')
    if not api_key or api_key == 'your_yelp_api_key_here':
        print("⚠️  SKIPPING: No valid API key found")
        print("   Set YELP_API_KEY environment variable to run integration test")
        return False
    
    try:
        analyzer = YelpReviewAnalyzer()
        
        # Test with a well-known business (Starbucks)
        print("Testing with Starbucks business search...")
        businesses = search_businesses("Starbucks", "New York, NY", api_key)
        
        if businesses:
            test_business = businesses[0]
            print(f"✅ Found test business: {test_business['name']}")
            print(f"   Business ID: {test_business['id']}")
            
            # Test getting business details
            details = get_business_details(test_business['id'], api_key)
            if details:
                print(f"✅ Got business details successfully")
                print(f"   Rating: {details.get('rating', 'N/A')}")
                print(f"   Review count: {details.get('review_count', 'N/A')}")
            
            return True
        else:
            print("❌ No businesses found in search")
            return False
            
    except Exception as e:
        print(f"❌ ERROR in integration test: {e}")
        return False


def main():
    """
    Run all tests
    """
    print("🧪 YELP REVIEW ANALYZER - TEST SUITE")
    print("=" * 60)
    print()
    
    tests = [
        ("Configuration Loading", test_config_loading),
        ("Without API Key", test_without_api_key),
        ("With Mock Data", test_with_mock_data),
        ("Business Search", test_business_search),
        ("Visualizer", test_visualizer),
        ("Integration Test", run_integration_test)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ ERROR in {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Your analyzer is ready to use.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")


if __name__ == "__main__":
    main()
