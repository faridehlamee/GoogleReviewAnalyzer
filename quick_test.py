"""
Quick test script for Yelp Review Analyzer
Run this for a fast test without API calls
"""
import os
import sys
from yelp_analyzer import YelpReviewAnalyzer
from visualizer import YelpDataVisualizer


def quick_test():
    """
    Quick test with simulated data
    """
    print("🚀 QUICK TEST - Yelp Review Analyzer")
    print("=" * 50)
    
    # Create analyzer with dummy API key
    analyzer = YelpReviewAnalyzer(api_key="dummy_key_for_testing")
    
    # Create sample review data
    sample_reviews = [
        {'rating': 5, 'text': 'Amazing food and service!', 'user': {'id': 'user1', 'name': 'Happy Customer'}},
        {'rating': 4, 'text': 'Good experience overall', 'user': {'id': 'user2', 'name': 'Satisfied Customer'}},
        {'rating': 2, 'text': 'Poor service, food was cold', 'user': {'id': 'user3', 'name': 'Disappointed Customer'}},
        {'rating': 1, 'text': 'Terrible experience, avoid this place', 'user': {'id': 'user4', 'name': 'Angry Customer'}},
        {'rating': 3, 'text': 'Average food, nothing special', 'user': {'id': 'user5', 'name': 'Neutral Customer'}},
    ]
    
    # Simulate user review data
    user_review_data = {
        'user3': [  # Disappointed Customer - mostly negative
            {'rating': 2, 'text': 'Bad service', 'business_id': 'biz1'},
            {'rating': 1, 'text': 'Awful food', 'business_id': 'biz2'},
            {'rating': 2, 'text': 'Poor quality', 'business_id': 'biz3'},
            {'rating': 1, 'text': 'Terrible', 'business_id': 'biz4'},
            {'rating': 2, 'text': 'Disappointing', 'business_id': 'biz5'},
            {'rating': 1, 'text': 'Worst ever', 'business_id': 'biz6'},
        ],
        'user4': [  # Angry Customer - all negative
            {'rating': 1, 'text': 'Horrible', 'business_id': 'biz7'},
            {'rating': 1, 'text': 'Terrible', 'business_id': 'biz8'},
            {'rating': 2, 'text': 'Bad', 'business_id': 'biz9'},
            {'rating': 1, 'text': 'Awful', 'business_id': 'biz10'},
            {'rating': 1, 'text': 'Worst', 'business_id': 'biz11'},
            {'rating': 1, 'text': 'Disgusting', 'business_id': 'biz12'},
            {'rating': 1, 'text': 'Never again', 'business_id': 'biz13'},
            {'rating': 2, 'text': 'Poor service', 'business_id': 'biz14'},
        ]
    }
    
    # Mock the API calls
    from unittest.mock import patch
    
    with patch.object(analyzer, 'get_business_reviews', return_value=sample_reviews):
        with patch.object(analyzer, 'get_user_reviews') as mock_user_reviews:
            def mock_user_reviews_side_effect(user_id):
                return user_review_data.get(user_id, [])
            
            mock_user_reviews.side_effect = mock_user_reviews_side_effect
            
            # Run the analysis
            print("📊 Running analysis...")
            results = analyzer.analyze_business_reviews("test_business")
            
            # Display results
            print("\n" + analyzer.generate_summary_report(results))
            
            # Test visualizer
            print("\n📈 Testing visualizer...")
            try:
                visualizer = YelpDataVisualizer(output_dir='test_output')
                visualizer.create_summary_dashboard(results, save=False)
                print("✅ Visualizer test successful!")
            except Exception as e:
                print(f"⚠️  Visualizer test failed: {e}")
    
    print("\n🎉 Quick test completed!")
    print("\nTo run a full test suite, use: python test_analyzer.py")


if __name__ == "__main__":
    quick_test()
