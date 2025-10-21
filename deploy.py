"""
Quick Deployment Script for Google Review Analyzer
"""
import os
import subprocess
import sys

def deploy_to_heroku():
    """Deploy to Heroku"""
    print("🚀 Deploying Google Review Analyzer to Heroku...")
    
    # Check if Heroku CLI is installed
    try:
        subprocess.run(["heroku", "--version"], check=True, capture_output=True)
        print("✅ Heroku CLI found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Heroku CLI not found. Please install from: https://devcenter.heroku.com/articles/heroku-cli")
        return False
    
    # Check if git is initialized
    if not os.path.exists(".git"):
        print("📁 Initializing git repository...")
        subprocess.run(["git", "init"], check=True)
    
    # Add all files
    print("📦 Adding files to git...")
    subprocess.run(["git", "add", "."], check=True)
    
    # Commit changes
    print("💾 Committing changes...")
    subprocess.run(["git", "commit", "-m", "Deploy Google Review Analyzer"], check=True)
    
    # Check if Heroku app exists
    try:
        subprocess.run(["heroku", "apps:info"], check=True, capture_output=True)
        print("✅ Heroku app found")
    except subprocess.CalledProcessError:
        print("🔧 Creating Heroku app...")
        app_name = input("Enter your desired app name (or press Enter for auto-generated): ").strip()
        if app_name:
            subprocess.run(["heroku", "create", app_name], check=True)
        else:
            subprocess.run(["heroku", "create"], check=True)
    
    # Set environment variables
    print("🔑 Setting up environment variables...")
    api_key = input("Enter your Google API key: ").strip()
    if api_key:
        subprocess.run(["heroku", "config:set", f"GOOGLE_API_KEY={api_key}"], check=True)
        print("✅ Google API key set")
    else:
        print("⚠️ No API key provided. You'll need to set it manually later.")
    
    # Deploy
    print("🚀 Deploying to Heroku...")
    subprocess.run(["git", "push", "heroku", "main"], check=True)
    
    # Open the app
    print("🌐 Opening your deployed app...")
    subprocess.run(["heroku", "open"], check=True)
    
    print("🎉 Deployment complete!")
    print("Your Google Review Analyzer is now live on the web!")
    return True

def main():
    """Main deployment function"""
    print("🌐 Google Review Analyzer - Deployment Helper")
    print("=" * 50)
    
    choice = input("Choose deployment platform:\n1. Heroku (Recommended)\n2. Manual instructions\nEnter choice (1-2): ").strip()
    
    if choice == "1":
        deploy_to_heroku()
    elif choice == "2":
        print("\n📋 Manual Deployment Instructions:")
        print("1. Go to https://heroku.com and create an account")
        print("2. Install Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli")
        print("3. Run: heroku login")
        print("4. Run: heroku create your-app-name")
        print("5. Run: heroku config:set GOOGLE_API_KEY=your_key_here")
        print("6. Run: git init")
        print("7. Run: git add .")
        print("8. Run: git commit -m 'Initial deployment'")
        print("9. Run: git push heroku main")
        print("10. Run: heroku open")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
