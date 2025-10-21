"""
Data visualization module for Yelp Review Analyzer
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List
import os


class YelpDataVisualizer:
    """
    Creates visualizations for Yelp review analysis data
    """
    
    def __init__(self, output_dir: str = 'output'):
        """
        Initialize visualizer
        
        Args:
            output_dir: Directory to save plots
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def plot_rating_distribution(self, results: Dict, save: bool = True) -> None:
        """
        Plot distribution of ratings for the target business
        
        Args:
            results: Analysis results dictionary
            save: Whether to save the plot
        """
        reviews = results.get('all_reviews', [])
        if not reviews:
            print("No reviews data available for plotting")
            return
        
        ratings = [review['rating'] for review in reviews]
        
        plt.figure(figsize=(10, 6))
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Rating histogram
        ax1.hist(ratings, bins=5, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_xlabel('Rating (Stars)')
        ax1.set_ylabel('Number of Reviews')
        ax1.set_title('Distribution of Ratings')
        ax1.set_xticks(range(1, 6))
        
        # Rating pie chart
        rating_counts = pd.Series(ratings).value_counts().sort_index()
        colors = ['red', 'orange', 'yellow', 'lightgreen', 'green']
        ax2.pie(rating_counts.values, labels=[f'{i} star{"s" if i > 1 else ""}' for i in rating_counts.index], 
                autopct='%1.1f%%', colors=colors[:len(rating_counts)])
        ax2.set_title('Rating Distribution')
        
        plt.tight_layout()
        
        if save:
            filename = os.path.join(self.output_dir, 'rating_distribution.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Rating distribution plot saved to: {filename}")
        
        plt.show()
    
    def plot_suspicious_users_analysis(self, results: Dict, save: bool = True) -> None:
        """
        Plot analysis of suspicious users
        
        Args:
            results: Analysis results dictionary
            save: Whether to save the plot
        """
        user_analysis = results.get('user_analysis', {})
        if not user_analysis:
            print("No user analysis data available for plotting")
            return
        
        # Prepare data
        data = []
        for user_id, user_data in user_analysis.items():
            data.append({
                'user_name': user_data['name'],
                'total_reviews': user_data['total_reviews'],
                'low_rating_percentage': user_data['low_rating_percentage'] * 100,
                'average_rating': user_data['average_rating'],
                'is_suspicious': user_data['is_suspicious']
            })
        
        df = pd.DataFrame(data)
        
        if df.empty:
            print("No data to plot")
            return
        
        # Create plots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Low rating percentage by user
        colors = ['red' if x else 'blue' for x in df['is_suspicious']]
        axes[0, 0].bar(range(len(df)), df['low_rating_percentage'], color=colors, alpha=0.7)
        axes[0, 0].set_xlabel('Users')
        axes[0, 0].set_ylabel('Low Rating Percentage (%)')
        axes[0, 0].set_title('Low Rating Percentage by User')
        axes[0, 0].axhline(y=70, color='red', linestyle='--', alpha=0.5, label='Suspicious Threshold (70%)')
        axes[0, 0].legend()
        
        # Average rating by user
        axes[0, 1].bar(range(len(df)), df['average_rating'], color=colors, alpha=0.7)
        axes[0, 1].set_xlabel('Users')
        axes[0, 1].set_ylabel('Average Rating Given')
        axes[0, 1].set_title('Average Rating Given by User')
        axes[0, 1].axhline(y=4, color='green', linestyle='--', alpha=0.5, label='High Rating Threshold (4 stars)')
        axes[0, 1].legend()
        
        # Total reviews vs low rating percentage
        scatter = axes[1, 0].scatter(df['total_reviews'], df['low_rating_percentage'], 
                                   c=colors, alpha=0.7, s=100)
        axes[1, 0].set_xlabel('Total Reviews')
        axes[1, 0].set_ylabel('Low Rating Percentage (%)')
        axes[1, 0].set_title('Total Reviews vs Low Rating Percentage')
        axes[1, 0].axhline(y=70, color='red', linestyle='--', alpha=0.5)
        
        # Summary statistics
        suspicious_count = df['is_suspicious'].sum()
        total_users = len(df)
        axes[1, 1].pie([suspicious_count, total_users - suspicious_count], 
                      labels=['Suspicious', 'Normal'], autopct='%1.1f%%',
                      colors=['red', 'green'], alpha=0.7)
        axes[1, 1].set_title(f'Suspicious Users Summary\n({suspicious_count}/{total_users} users)')
        
        plt.tight_layout()
        
        if save:
            filename = os.path.join(self.output_dir, 'suspicious_users_analysis.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Suspicious users analysis plot saved to: {filename}")
        
        plt.show()
    
    def plot_user_rating_patterns(self, results: Dict, save: bool = True) -> None:
        """
        Plot individual user rating patterns
        
        Args:
            results: Analysis results dictionary
            save: Whether to save the plot
        """
        user_analysis = results.get('user_analysis', {})
        if not user_analysis:
            print("No user analysis data available for plotting")
            return
        
        # Create a plot for each user
        n_users = len(user_analysis)
        if n_users == 0:
            return
        
        fig, axes = plt.subplots((n_users + 1) // 2, 2, figsize=(15, 5 * ((n_users + 1) // 2)))
        if n_users == 1:
            axes = [axes]
        elif n_users <= 2:
            axes = axes.reshape(1, -1)
        
        axes = axes.flatten()
        
        for i, (user_id, user_data) in enumerate(user_analysis.items()):
            if i >= len(axes):
                break
                
            ratings = user_data['all_ratings']
            is_suspicious = user_data['is_suspicious']
            
            # Create histogram of user's ratings
            rating_counts = pd.Series(ratings).value_counts().sort_index()
            colors = ['red', 'orange', 'yellow', 'lightgreen', 'green']
            bars = axes[i].bar(rating_counts.index, rating_counts.values, 
                             color=[colors[r-1] for r in rating_counts.index], alpha=0.7)
            
            axes[i].set_xlabel('Rating Given')
            axes[i].set_ylabel('Number of Reviews')
            axes[i].set_title(f"{user_data['name']} {'(SUSPICIOUS)' if is_suspicious else ''}")
            axes[i].set_xticks(range(1, 6))
            
            # Add average line
            avg_rating = user_data['average_rating']
            axes[i].axvline(x=avg_rating, color='red', linestyle='--', alpha=0.8, 
                           label=f'Average: {avg_rating:.1f}')
            axes[i].legend()
        
        # Hide unused subplots
        for i in range(n_users, len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        
        if save:
            filename = os.path.join(self.output_dir, 'user_rating_patterns.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"User rating patterns plot saved to: {filename}")
        
        plt.show()
    
    def create_summary_dashboard(self, results: Dict, save: bool = True) -> None:
        """
        Create a comprehensive summary dashboard
        
        Args:
            results: Analysis results dictionary
            save: Whether to save the plot
        """
        fig = plt.figure(figsize=(20, 12))
        
        # Create a grid layout
        gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
        
        # Main title
        fig.suptitle(f'Yelp Review Analysis Dashboard - Business ID: {results.get("business_id", "Unknown")}', 
                    fontsize=16, fontweight='bold')
        
        # 1. Overall statistics
        ax1 = fig.add_subplot(gs[0, 0])
        total_reviews = results.get('total_reviews', 0)
        low_rating_reviews = results.get('low_rating_reviews', 0)
        suspicious_users = results.get('suspicious_users_count', 0)
        
        stats_text = f"""Overall Statistics:
Total Reviews: {total_reviews}
Low Rating Reviews: {low_rating_reviews}
Suspicious Users: {suspicious_users}
Low Rating %: {(low_rating_reviews/total_reviews*100):.1f}%"""
        
        ax1.text(0.1, 0.5, stats_text, transform=ax1.transAxes, fontsize=12, 
                verticalalignment='center', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        ax1.axis('off')
        
        # 2. Rating distribution pie chart
        ax2 = fig.add_subplot(gs[0, 1])
        reviews = results.get('all_reviews', [])
        if reviews:
            ratings = [review['rating'] for review in reviews]
            rating_counts = pd.Series(ratings).value_counts().sort_index()
            colors = ['red', 'orange', 'yellow', 'lightgreen', 'green']
            ax2.pie(rating_counts.values, labels=[f'{i}★' for i in rating_counts.index], 
                   autopct='%1.1f%%', colors=colors[:len(rating_counts)])
            ax2.set_title('Rating Distribution')
        
        # 3. Suspicious users summary
        ax3 = fig.add_subplot(gs[0, 2])
        user_analysis = results.get('user_analysis', {})
        if user_analysis:
            suspicious_count = sum(1 for u in user_analysis.values() if u['is_suspicious'])
            normal_count = len(user_analysis) - suspicious_count
            ax3.pie([suspicious_count, normal_count], 
                   labels=['Suspicious', 'Normal'], autopct='%1.1f%%',
                   colors=['red', 'green'])
            ax3.set_title('User Classification')
        
        # 4. Low rating percentage distribution
        ax4 = fig.add_subplot(gs[0, 3])
        if user_analysis:
            low_rating_percentages = [u['low_rating_percentage'] * 100 for u in user_analysis.values()]
            ax4.hist(low_rating_percentages, bins=10, alpha=0.7, color='orange', edgecolor='black')
            ax4.set_xlabel('Low Rating Percentage (%)')
            ax4.set_ylabel('Number of Users')
            ax4.set_title('Low Rating Percentage Distribution')
            ax4.axvline(x=70, color='red', linestyle='--', alpha=0.8, label='Suspicious Threshold')
            ax4.legend()
        
        # 5-6. User analysis table (spans 2 columns)
        ax5 = fig.add_subplot(gs[1, :2])
        if user_analysis:
            # Create a table with user data
            table_data = []
            for user_id, user_data in user_analysis.items():
                table_data.append([
                    user_data['name'][:15] + "..." if len(user_data['name']) > 15 else user_data['name'],
                    f"{user_data['total_reviews']}",
                    f"{user_data['low_rating_percentage']:.1%}",
                    f"{user_data['average_rating']:.1f}",
                    "⚠️" if user_data['is_suspicious'] else "✅"
                ])
            
            table = ax5.table(cellText=table_data,
                            colLabels=['User Name', 'Total Reviews', 'Low Rating %', 'Avg Rating', 'Status'],
                            cellLoc='center',
                            loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1.2, 1.5)
            ax5.axis('off')
            ax5.set_title('User Analysis Summary')
        
        # 7. Average ratings comparison
        ax6 = fig.add_subplot(gs[1, 2:])
        if user_analysis:
            user_names = [u['name'][:10] + "..." if len(u['name']) > 10 else u['name'] for u in user_analysis.values()]
            avg_ratings = [u['average_rating'] for u in user_analysis.values()]
            colors = ['red' if u['is_suspicious'] else 'blue' for u in user_analysis.values()]
            
            bars = ax6.bar(range(len(user_names)), avg_ratings, color=colors, alpha=0.7)
            ax6.set_xlabel('Users')
            ax6.set_ylabel('Average Rating Given')
            ax6.set_title('Average Rating Given by Each User')
            ax6.set_xticks(range(len(user_names)))
            ax6.set_xticklabels(user_names, rotation=45, ha='right')
            ax6.axhline(y=4, color='green', linestyle='--', alpha=0.5, label='High Rating Threshold')
            ax6.legend()
        
        # 8. Recommendations
        ax7 = fig.add_subplot(gs[2, :])
        recommendations = self._generate_recommendations(results)
        ax7.text(0.05, 0.5, recommendations, transform=ax7.transAxes, fontsize=11, 
                verticalalignment='center', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))
        ax7.set_xlim(0, 1)
        ax7.set_ylim(0, 1)
        ax7.axis('off')
        
        if save:
            filename = os.path.join(self.output_dir, 'analysis_dashboard.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Analysis dashboard saved to: {filename}")
        
        plt.show()
    
    def _generate_recommendations(self, results: Dict) -> str:
        """
        Generate recommendations based on analysis results
        
        Args:
            results: Analysis results dictionary
            
        Returns:
            Recommendations string
        """
        recommendations = "RECOMMENDATIONS:\n\n"
        
        suspicious_count = results.get('suspicious_users_count', 0)
        total_reviews = results.get('total_reviews', 0)
        low_rating_reviews = results.get('low_rating_reviews', 0)
        
        if suspicious_count == 0:
            recommendations += "✅ No suspicious reviewers found. Your business appears to have genuine reviews.\n"
        elif suspicious_count <= 2:
            recommendations += f"⚠️ Found {suspicious_count} potentially suspicious reviewer(s). Monitor these users for future reviews.\n"
        else:
            recommendations += f"🚨 Found {suspicious_count} suspicious reviewers. Consider reporting these users to Yelp for review.\n"
        
        low_rating_percentage = (low_rating_reviews / total_reviews * 100) if total_reviews > 0 else 0
        
        if low_rating_percentage > 30:
            recommendations += f"\n📊 High percentage of low ratings ({low_rating_percentage:.1f}%). This could indicate:\n"
            recommendations += "   • Genuine quality issues that need addressing\n"
            recommendations += "   • Targeted negative reviews from competitors\n"
            recommendations += "   • Unfair reviews from suspicious users\n"
        elif low_rating_percentage < 10:
            recommendations += f"\n📊 Low percentage of low ratings ({low_rating_percentage:.1f}%). Your business appears to be well-received.\n"
        else:
            recommendations += f"\n📊 Moderate percentage of low ratings ({low_rating_percentage:.1f}%). Monitor for patterns.\n"
        
        recommendations += "\n💡 NEXT STEPS:\n"
        recommendations += "1. Review the detailed reports in the 'reports' directory\n"
        recommendations += "2. Address any legitimate quality concerns raised in reviews\n"
        recommendations += "3. Consider reporting suspicious users to Yelp\n"
        recommendations += "4. Monitor future reviews for similar patterns\n"
        
        return recommendations


def main():
    """
    Example usage of the visualizer
    """
    import json
    
    # Load sample results (you would load from your actual analysis)
    try:
        with open('output/latest_results.json', 'r') as f:
            results = json.load(f)
        
        visualizer = YelpDataVisualizer()
        visualizer.create_summary_dashboard(results)
        
    except FileNotFoundError:
        print("No analysis results found. Run the main analyzer first.")
        print("Example: python main.py your_business_id")


if __name__ == "__main__":
    main()
