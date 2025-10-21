"""
Setup script for Yelp Review Analyzer
"""
import os
import subprocess
import sys


def install_requirements():
    """
    Install required packages
    """
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False


def create_directories():
    """
    Create necessary directories
    """
    directories = ['output', 'reports', 'data']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")


def create_env_file():
    """
    Create .env file from template
    """
    if not os.path.exists('.env'):
        if os.path.exists('env_example.txt'):
            with open('env_example.txt', 'r') as f:
                content = f.read()
            
            with open('.env', 'w') as f:
                f.write(content)
            
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file and add your Yelp API key!")
        else:
            print("❌ env_example.txt not found")
    else:
        print("📁 .env file already exists")


def verify_api_key():
    """
    Verify if API key is set
    """
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('YELP_API_KEY')
        if api_key and api_key != 'your_yelp_api_key_here':
            print("✅ Yelp API key is configured")
            return True
        else:
            print("⚠️  Yelp API key not configured")
            print("   Please edit .env file and add your API key")
            return False
    except ImportError:
        print("⚠️  python-dotenv not installed, cannot verify API key")
        return False


def main():
    """
    Main setup function
    """
    print("🔧 YELP REVIEW ANALYZER SETUP")
    print("=" * 40)
    print()
    
    # Install requirements
    if not install_requirements():
        print("Setup failed. Please install requirements manually.")
        return False
    
    print()
    
    # Create directories
    print("Creating directories...")
    create_directories()
    print()
    
    # Create .env file
    print("Setting up environment...")
    create_env_file()
    print()
    
    # Verify API key
    verify_api_key()
    print()
    
    print("🎉 SETUP COMPLETE!")
    print("=" * 40)
    print()
    print("Next steps:")
    print("1. Get your Yelp API key from: https://www.yelp.com/developers/documentation/v3/authentication")
    print("2. Edit the .env file and add your API key")
    print("3. Run: python main.py <business_id>")
    print("4. Or run: python example_usage.py")
    print()
    print("For help finding business IDs, run: python utils.py")
    
    return True


if __name__ == "__main__":
    main()
