"""
Main entry point for Google Places Review Analyzer
"""
import sys
import argparse
from yelp_analyzer import GooglePlacesReviewAnalyzer


def main():
    """
    Main function with command line interface
    """
    parser = argparse.ArgumentParser(description='Analyze Google Places reviews to identify suspicious reviewers')
    parser.add_argument('place_id', help='Google Places place ID to analyze')
    parser.add_argument('--api-key', help='Google Places API key (overrides config.py)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    try:
        print("Google Places Review Analyzer")
        print("=" * 50)
        
        analyzer = GooglePlacesReviewAnalyzer(api_key=args.api_key)
        
        if args.verbose:
            print(f"Analyzing place ID: {args.place_id}")
            print("This may take a few minutes depending on the number of reviews...")
        
        results = analyzer.analyze_business_reviews(args.place_id)
        
        if 'error' in results:
            print(f"❌ Error: {results['error']}")
            return 1
        
        # Print summary report
        print("\n" + analyzer.generate_summary_report(results))
        
        print("\n✅ Analysis complete!")
        print("Check the 'output' and 'reports' directories for detailed results.")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️  Analysis interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
