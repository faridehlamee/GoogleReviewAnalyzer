"""
Google Places Review Analyzer - Main class for analyzing Google Places reviews and identifying suspicious reviewers
Updated to use Google Places API instead of Yelp due to Yelp's new paid-only model
"""
import requests
import pandas as pd
import time
import json
import os
from typing import List, Dict, Optional, Tuple
from config import (
    GOOGLE_API_KEY, LOW_RATING_THRESHOLD, 
    MIN_REVIEWS_FOR_ANALYSIS, SUSPICIOUS_THRESHOLD, 
    DELAY_BETWEEN_REQUESTS, OUTPUT_DIR, REPORTS_DIR
)


class GooglePlacesReviewAnalyzer:
    """
    Analyzes Google Places reviews to identify users with suspicious review patterns
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the analyzer with Google Places API key
        
        Args:
            api_key: Google Places API key. If None, uses config.py value
        """
        self.api_key = api_key or GOOGLE_API_KEY
        if not self.api_key:
            raise ValueError("Google Places API key is required. Set GOOGLE_API_KEY in config.py or pass api_key parameter")
        
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        
        # Create output directories
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        os.makedirs(REPORTS_DIR, exist_ok=True)
        
        # Cache for user reviews to avoid repeated API calls
        self.user_reviews_cache = {}
        
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """
        Make a request to Google Places API with rate limiting
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            JSON response data
        """
        time.sleep(DELAY_BETWEEN_REQUESTS)
        
        params = params or {}
        params['key'] = self.api_key
        url = f"{self.base_url}/{endpoint}"
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_business_reviews(self, place_id: str) -> List[Dict]:
        """
        Get all reviews for a specific business
        
        Args:
            place_id: Google Places place ID
            
        Returns:
            List of review dictionaries
        """
        params = {
            'place_id': place_id,
            'fields': 'place_id,name,rating,user_ratings_total,formatted_address,reviews'
        }
        
        try:
            data = self._make_request('details/json', params)
            business_details = data.get('result', {})
            
            if not business_details:
                return []
            
            reviews = business_details.get('reviews', [])
            
            # Convert Google Places format to our standard format
            formatted_reviews = []
            for review in reviews:
                formatted_review = {
                    'rating': review.get('rating', 0),
                    'text': review.get('text', ''),
                    'user': {
                        'id': review.get('author_name', 'Unknown'),
                        'name': review.get('author_name', 'Unknown')
                    },
                    'time_created': review.get('time', 0),
                    'profile_photo_url': review.get('profile_photo_url', '')
                }
                formatted_reviews.append(formatted_review)
            
            return formatted_reviews
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching reviews: {e}")
            return []
    
    def get_user_reviews(self, user_name: str) -> List[Dict]:
        """
        Get all reviews from a specific user (Note: This is limited by Google Places API)
        For demonstration, we'll simulate this functionality
        
        Args:
            user_name: Google user name
            
        Returns:
            List of user's review dictionaries
        """
        # Note: Google Places API doesn't provide direct access to all reviews by a user
        # This is a limitation of the public API. In a real implementation, you might:
        # 1. Use web scraping (with proper permissions and rate limiting)
        # 2. Build a database of reviews over time
        # 3. Use other data sources
        
        # For now, we'll return cached data if available
        if user_name in self.user_reviews_cache:
            return self.user_reviews_cache[user_name]
        
        # Simulate user review data (in practice, this would come from your data source)
        # This is just for demonstration purposes
        simulated_reviews = self._simulate_user_reviews(user_name)
        self.user_reviews_cache[user_name] = simulated_reviews
        
        return simulated_reviews
    
    def _simulate_user_reviews(self, user_id: str) -> List[Dict]:
        """
        Simulate user reviews for demonstration purposes
        In a real implementation, this would be replaced with actual data collection
        """
        import random
        
        # Simulate different types of users
        if hash(user_id) % 3 == 0:  # 33% chance of being a "negative reviewer"
            # User tends to give low ratings
            ratings = [random.choice([1, 2, 3]) for _ in range(random.randint(5, 15))]
        elif hash(user_id) % 3 == 1:  # 33% chance of being a "positive reviewer"
            # User tends to give high ratings
            ratings = [random.choice([4, 5]) for _ in range(random.randint(5, 15))]
        else:  # 33% chance of being a "mixed reviewer"
            # User gives mixed ratings
            ratings = [random.choice([1, 2, 3, 4, 5]) for _ in range(random.randint(5, 15))]
        
        reviews = []
        for i, rating in enumerate(ratings):
            reviews.append({
                'rating': rating,
                'text': f"Review {i+1} by {user_id}",
                'business_id': f"business_{random.randint(1, 100)}",
                'business_name': f"Business {random.randint(1, 100)}",
                'time_created': f"2023-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}T{random.randint(10, 23):02d}:00:00Z"
            })
        
        return reviews
    
    def analyze_business_reviews(self, place_id: str) -> Dict:
        """
        Main analysis function - analyzes reviews for a business and identifies suspicious reviewers
        
        Args:
            place_id: Google Places place ID to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        print(f"Fetching reviews for place ID {place_id}...")
        
        # Get all reviews for the business
        reviews = self.get_business_reviews(place_id)
        
        if not reviews:
            return {"error": "No reviews found for this business"}
        
        # Convert to DataFrame for easier analysis
        df_reviews = pd.DataFrame(reviews)
        
        # Extract reviewer information
        df_reviews['reviewer_id'] = df_reviews['user'].apply(lambda x: x['id'])
        df_reviews['reviewer_name'] = df_reviews['user'].apply(lambda x: x['name'])
        df_reviews['reviewer_image_url'] = df_reviews['user'].apply(lambda x: x.get('image_url', ''))
        
        # Identify low-rating reviewers
        low_rating_reviewers = df_reviews[df_reviews['rating'] < LOW_RATING_THRESHOLD]
        
        print(f"Found {len(low_rating_reviewers)} reviews with rating < {LOW_RATING_THRESHOLD} stars")
        print(f"Total reviews analyzed: {len(df_reviews)}")
        
        # Analyze each low-rating reviewer
        suspicious_users = []
        user_analysis = {}
        
        for _, review in low_rating_reviewers.iterrows():
            user_id = review['reviewer_id']
            user_name = review['reviewer_name']
            
            print(f"Analyzing user: {user_name} (ID: {user_id})")
            
            # Get all reviews from this user
            user_reviews = self.get_user_reviews(user_id)
            
            if len(user_reviews) >= MIN_REVIEWS_FOR_ANALYSIS:
                # Analyze user's review pattern
                user_ratings = [r['rating'] for r in user_reviews]
                low_rating_count = sum(1 for rating in user_ratings if rating < LOW_RATING_THRESHOLD)
                low_rating_percentage = low_rating_count / len(user_ratings)
                
                user_analysis[user_id] = {
                    'name': user_name,
                    'total_reviews': len(user_reviews),
                    'low_rating_count': low_rating_count,
                    'low_rating_percentage': low_rating_percentage,
                    'average_rating': sum(user_ratings) / len(user_ratings),
                    'all_ratings': user_ratings,
                    'is_suspicious': low_rating_percentage >= SUSPICIOUS_THRESHOLD,
                    'target_business_rating': review['rating'],
                    'target_business_comment': review.get('text', '')
                }
                
                if low_rating_percentage >= SUSPICIOUS_THRESHOLD:
                    suspicious_users.append(user_id)
                    print(f"  [SUSPICIOUS] {low_rating_percentage:.1%} of reviews are low ratings")
                else:
                    print(f"  [NORMAL] {low_rating_percentage:.1%} of reviews are low ratings")
        
        # Generate summary
        results = {
            'place_id': place_id,
            'total_reviews': len(df_reviews),
            'low_rating_reviews': len(low_rating_reviewers),
            'suspicious_users_count': len(suspicious_users),
            'user_analysis': user_analysis,
            'suspicious_users': suspicious_users,
            'all_reviews': df_reviews.to_dict('records')
        }
        
        # Save results
        self._save_results(results)
        
        return results
    
    def _save_results(self, results: Dict):
        """
        Save analysis results to files
        
        Args:
            results: Analysis results dictionary
        """
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results as JSON
        results_file = os.path.join(OUTPUT_DIR, f"analysis_results_{timestamp}.json")
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Save suspicious users report
        if results['suspicious_users']:
            report_file = os.path.join(REPORTS_DIR, f"suspicious_users_{timestamp}.txt")
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("SUSPICIOUS GOOGLE PLACES REVIEWERS REPORT\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Place ID: {results['place_id']}\n")
                f.write(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Reviews: {results['total_reviews']}\n")
                f.write(f"Low Rating Reviews: {results['low_rating_reviews']}\n")
                f.write(f"Suspicious Users Found: {results['suspicious_users_count']}\n\n")
                
                for user_id in results['suspicious_users']:
                    user_data = results['user_analysis'][user_id]
                    f.write(f"User: {user_data['name']} (ID: {user_id})\n")
                    f.write(f"  Total Reviews: {user_data['total_reviews']}\n")
                    f.write(f"  Low Rating Percentage: {user_data['low_rating_percentage']:.1%}\n")
                    f.write(f"  Average Rating: {user_data['average_rating']:.1f}\n")
                    f.write(f"  Rating for Target Business: {user_data['target_business_rating']} stars\n")
                    f.write(f"  Comment: {user_data['target_business_comment'][:100]}...\n\n")
        
        print(f"Results saved to: {results_file}")
        if results['suspicious_users']:
            print(f"Report saved to: {report_file}")
    
    def generate_summary_report(self, results: Dict) -> str:
        """
        Generate a human-readable summary report
        
        Args:
            results: Analysis results dictionary
            
        Returns:
            Formatted summary string
        """
        report = f"""
GOOGLE PLACES REVIEW ANALYSIS SUMMARY
{'=' * 50}

Place ID: {results['place_id']}
Total Reviews Analyzed: {results['total_reviews']}
Reviews with Low Ratings (< {LOW_RATING_THRESHOLD} stars): {results['low_rating_reviews']}
Suspicious Users Identified: {results['suspicious_users_count']}

SUSPICIOUS REVIEWERS:
"""
        
        if results['suspicious_users']:
            for user_id in results['suspicious_users']:
                user_data = results['user_analysis'][user_id]
                report += f"""
- {user_data['name']} (ID: {user_id})
  • Total Reviews: {user_data['total_reviews']}
  • Low Rating Percentage: {user_data['low_rating_percentage']:.1%}
  • Average Rating Given: {user_data['average_rating']:.1f}/5.0
  • Rating for This Business: {user_data['target_business_rating']}/5.0
  • Comment: "{user_data['target_business_comment'][:100]}..."
"""
        else:
            report += "\nNo suspicious reviewers found.\n"
        
        return report


def main():
    """
    Example usage of the GooglePlacesReviewAnalyzer
    """
    # Example place ID (replace with actual place ID)
    place_id = "ChIJN1t_tDeuEmsRUsoyG83frY4"  # This is a sample Google Places ID
    
    try:
        analyzer = GooglePlacesReviewAnalyzer()
        results = analyzer.analyze_business_reviews(place_id)
        
        # Print summary
        print(analyzer.generate_summary_report(results))
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have set your Google Places API key in config.py or .env file")


if __name__ == "__main__":
    main()
