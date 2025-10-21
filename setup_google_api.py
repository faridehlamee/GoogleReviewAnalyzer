"""
Google Places API Setup Helper
This script helps you set up your Google Places API key
"""
import os


def setup_google_api():
    """
    Interactive setup for Google Places API key
    """
    print("GOOGLE PLACES API SETUP HELPER")
    print("=" * 50)
    print()
    
    print("Follow these steps to get your Google Places API key:")
    print()
    
    print("1. Go to Google Cloud Console:")
    print("   https://console.cloud.google.com/")
    print()
    
    print("2. Create a new project (or select existing)")
    print("   - Click project dropdown at top")
    print("   - Click 'New Project'")
    print("   - Enter project name")
    print("   - Click 'Create'")
    print()
    
    print("3. Enable billing (required even for free tier)")
    print("   - Go to 'Billing' in left menu")
    print("   - Link a billing account")
    print("   - You won't be charged for first 1,000 requests/month")
    print()
    
    print("4. Enable Places API")
    print("   - Go to 'APIs & Services' > 'Library'")
    print("   - Search for 'Places API'")
    print("   - Click 'Enable'")
    print()
    
    print("5. Create API Key")
    print("   - Go to 'APIs & Services' > 'Credentials'")
    print("   - Click 'Create Credentials' > 'API Key'")
    print("   - Copy the API key")
    print()
    
    print("6. Add API key to your project")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("   - .env file already exists")
        with open('.env', 'r') as f:
            content = f.read()
            if 'GOOGLE_API_KEY' in content:
                print("   - GOOGLE_API_KEY already set in .env file")
            else:
                print("   - Add this line to your .env file:")
                print("     GOOGLE_API_KEY=your_actual_api_key_here")
    else:
        print("   - Create .env file and add:")
        print("     GOOGLE_API_KEY=your_actual_api_key_here")
    
    print()
    
    # Ask if user wants to enter API key now
    api_key = input("Enter your Google Places API key (or press Enter to skip): ").strip()
    
    if api_key:
        # Create or update .env file
        env_content = f"GOOGLE_API_KEY={api_key}\n"
        
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                existing_content = f.read()
            
            if 'GOOGLE_API_KEY' in existing_content:
                # Update existing key
                lines = existing_content.split('\n')
                new_lines = []
                for line in lines:
                    if line.startswith('GOOGLE_API_KEY='):
                        new_lines.append(f"GOOGLE_API_KEY={api_key}")
                    else:
                        new_lines.append(line)
                env_content = '\n'.join(new_lines)
            else:
                # Add new key
                env_content = existing_content + f"\nGOOGLE_API_KEY={api_key}\n"
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ API key saved to .env file!")
        print()
        print("Now you can test your setup:")
        print("  python test_google_analyzer.py")
    else:
        print("No API key entered. You can add it later to .env file.")
    
    print()
    print("IMPORTANT NOTES:")
    print("- Google requires billing to be enabled even for free tier")
    print("- You get 1,000 free requests per month")
    print("- Additional requests cost $5 per 1,000")
    print("- Much cheaper than Yelp's $229/month minimum!")
    print()
    print("Need help? Check GOOGLE_SETUP_GUIDE.md for detailed instructions.")


def test_api_key():
    """
    Test if API key is working
    """
    print("TESTING GOOGLE PLACES API KEY")
    print("=" * 40)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ No API key found in .env file")
        print("Run setup_google_api.py first to set up your API key")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    # Test API key with a simple request
    try:
        import requests
        
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': 'Starbucks New York',
            'key': api_key
        }
        
        print("Testing API key with a simple search...")
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'OK':
                print("✅ API key is working correctly!")
                print(f"Found {len(data.get('results', []))} results")
                return True
            else:
                print(f"❌ API error: {data.get('error_message', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API key: {e}")
        return False


def main():
    """
    Main function
    """
    print("Choose an option:")
    print("1. Setup Google Places API key")
    print("2. Test existing API key")
    print("3. Both")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == '1':
        setup_google_api()
    elif choice == '2':
        test_api_key()
    elif choice == '3':
        setup_google_api()
        print("\n" + "="*50 + "\n")
        test_api_key()
    else:
        print("Invalid choice. Please run again and choose 1-3.")


if __name__ == "__main__":
    main()
