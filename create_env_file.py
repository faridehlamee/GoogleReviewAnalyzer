"""
Simple script to create .env file with Google API key
"""
import os

def create_env_file():
    """
    Create .env file with Google API key
    """
    print("Creating .env file for Google Places API key...")
    
    # Get API key from user
    api_key = input("Enter your Google Places API key: ").strip()
    
    if not api_key:
        print("No API key entered. Exiting.")
        return
    
    # Create .env file content
    env_content = f"""# Google Places API Configuration
# Get your API key from: https://console.cloud.google.com/
GOOGLE_API_KEY={api_key}
"""
    
    # Write to .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")
    print(f"API key saved: {api_key[:10]}...")
    print()
    print("Now you can test your setup:")
    print("  python test_google_analyzer.py")

if __name__ == "__main__":
    create_env_file()
