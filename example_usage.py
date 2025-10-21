"""
Example usage script for Yelp Review Analyzer
This demonstrates how to use the analyzer for different scenarios
"""
import os
import json
from yelp_analyzer import YelpReviewAnalyzer
from utils import interactive_business_search, export_results_to_csv
from visualizer import YelpDataVisualizer


def example_1_basic_analysis():
    """
    Example 1: Basic analysis of a business
    """
    print("=" * 60)
    print("EXAMPLE 1: Basic Business Analysis")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = YelpReviewAnalyzer()
    
    # Example business ID (replace with actual business ID)
    business_id = "4kMBvIEWPxWkWKFN__8SxQ"  # This is a sample ID
    
    try:
        # Analyze the business
        results = analyzer.analyze_business_reviews(business_id)
        
        if 'error' in results:
            print(f"Error: {results['error']}")
            return
        
        # Print summary
        print(analyzer.generate_summary_report(results))
        
        # Export to CSV
        export_results_to_csv(results, "example_basic_analysis.csv")
        
    except Exception as e:
        print(f"Error in basic analysis: {e}")


def example_2_interactive_search():
    """
    Example 2: Interactive business search and analysis
    """
    print("=" * 60)
    print("EXAMPLE 2: Interactive Business Search")
    print("=" * 60)
    
    # Interactive business search
    business_id = interactive_business_search()
    
    if business_id:
        analyzer = YelpReviewAnalyzer()
        results = analyzer.analyze_business_reviews(business_id)
        
        if 'error' not in results:
            print(analyzer.generate_summary_report(results))
        else:
            print(f"Error: {results['error']}")


def example_3_with_visualizations():
    """
    Example 3: Analysis with visualizations
    """
    print("=" * 60)
    print("EXAMPLE 3: Analysis with Visualizations")
    print("=" * 60)
    
    # Initialize analyzer and visualizer
    analyzer = YelpReviewAnalyzer()
    visualizer = YelpDataVisualizer()
    
    # Example business ID
    business_id = "4kMBvIEWPxWkWKFN__8SxQ"
    
    try:
        # Analyze the business
        results = analyzer.analyze_business_reviews(business_id)
        
        if 'error' in results:
            print(f"Error: {results['error']}")
            return
        
        # Create visualizations
        print("Creating visualizations...")
        visualizer.plot_rating_distribution(results)
        visualizer.plot_suspicious_users_analysis(results)
        visualizer.plot_user_rating_patterns(results)
        visualizer.create_summary_dashboard(results)
        
        print("Visualizations complete!")
        
    except Exception as e:
        print(f"Error in visualization example: {e}")


def example_4_batch_analysis():
    """
    Example 4: Batch analysis of multiple businesses
    """
    print("=" * 60)
    print("EXAMPLE 4: Batch Analysis")
    print("=" * 60)
    
    # List of business IDs to analyze
    business_ids = [
        "4kMBvIEWPxWkWKFN__8SxQ",  # Replace with actual business IDs
        # Add more business IDs here
    ]
    
    analyzer = YelpReviewAnalyzer()
    batch_results = {}
    
    for i, business_id in enumerate(business_ids, 1):
        print(f"\nAnalyzing business {i}/{len(business_ids)}: {business_id}")
        
        try:
            results = analyzer.analyze_business_reviews(business_id)
            batch_results[business_id] = results
            
            if 'error' not in results:
                print(f"  ✅ Analysis complete: {results['suspicious_users_count']} suspicious users found")
            else:
                print(f"  ❌ Error: {results['error']}")
                
        except Exception as e:
            print(f"  ❌ Error analyzing {business_id}: {e}")
    
    # Save batch results
    with open('batch_analysis_results.json', 'w') as f:
        json.dump(batch_results, f, indent=2)
    
    print(f"\nBatch analysis complete! Results saved to batch_analysis_results.json")


def example_5_custom_analysis():
    """
    Example 5: Custom analysis with modified parameters
    """
    print("=" * 60)
    print("EXAMPLE 5: Custom Analysis")
    print("=" * 60)
    
    # Create a custom analyzer with different thresholds
    from config import LOW_RATING_THRESHOLD, SUSPICIOUS_THRESHOLD
    
    # Temporarily modify config values for this example
    original_low_threshold = LOW_RATING_THRESHOLD
    original_suspicious_threshold = SUSPICIOUS_THRESHOLD
    
    # Custom thresholds
    custom_low_threshold = 3  # Consider ratings below 3 as "low"
    custom_suspicious_threshold = 0.8  # 80% low ratings = suspicious
    
    print(f"Using custom thresholds:")
    print(f"  Low rating threshold: < {custom_low_threshold} stars")
    print(f"  Suspicious threshold: {custom_suspicious_threshold:.0%} low ratings")
    
    # Note: In a real implementation, you would modify the analyzer class
    # to accept these parameters. For this example, we'll use the default values.
    
    analyzer = YelpReviewAnalyzer()
    business_id = "4kMBvIEWPxWkWKFN__8SxQ"
    
    try:
        results = analyzer.analyze_business_reviews(business_id)
        
        if 'error' not in results:
            print(analyzer.generate_summary_report(results))
        else:
            print(f"Error: {results['error']}")
            
    except Exception as e:
        print(f"Error in custom analysis: {e}")


def main():
    """
    Main function to run examples
    """
    print("🍽️  YELP REVIEW ANALYZER - EXAMPLE USAGE")
    print("=" * 60)
    print()
    print("Choose an example to run:")
    print("1. Basic Analysis")
    print("2. Interactive Business Search")
    print("3. Analysis with Visualizations")
    print("4. Batch Analysis")
    print("5. Custom Analysis")
    print("6. Run All Examples")
    print()
    
    choice = input("Enter your choice (1-6): ").strip()
    
    if choice == "1":
        example_1_basic_analysis()
    elif choice == "2":
        example_2_interactive_search()
    elif choice == "3":
        example_3_with_visualizations()
    elif choice == "4":
        example_4_batch_analysis()
    elif choice == "5":
        example_5_custom_analysis()
    elif choice == "6":
        print("Running all examples...")
        example_1_basic_analysis()
        example_3_with_visualizations()
        example_4_batch_analysis()
    else:
        print("Invalid choice. Please run the script again and choose 1-6.")
    
    print("\n✅ Examples complete!")


if __name__ == "__main__":
    main()
