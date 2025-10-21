"""
Railway Deployment Helper - Push to GitHub
"""
import subprocess
import os

def setup_github_repo():
    """Help set up GitHub repository for Railway deployment"""
    print("🚂 Railway Deployment Helper")
    print("=" * 40)
    
    print("\n📋 Steps to deploy to Railway:")
    print("1. Create a new repository on GitHub")
    print("2. Copy the repository URL")
    print("3. Run the commands below")
    
    repo_url = input("\n🔗 Enter your GitHub repository URL (e.g., https://github.com/username/repo-name.git): ").strip()
    
    if not repo_url:
        print("❌ No repository URL provided")
        return False
    
    try:
        print("\n🔄 Setting up GitHub remote...")
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
        
        print("📤 Pushing to GitHub...")
        subprocess.run(["git", "branch", "-M", "main"], check=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        
        print("\n✅ Successfully pushed to GitHub!")
        print("\n🚂 Next steps:")
        print("1. Go to https://railway.app")
        print("2. Sign in with your account")
        print("3. Click 'New Project'")
        print("4. Select 'Deploy from GitHub repo'")
        print("5. Choose your repository")
        print("6. Add environment variable: GOOGLE_API_KEY")
        print("7. Your app will be live in 2-3 minutes!")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure:")
        print("- You have a GitHub repository created")
        print("- The repository URL is correct")
        print("- You have git configured with your credentials")
        return False

def main():
    """Main function"""
    print("🌐 Google Review Analyzer - Railway Deployment")
    print("=" * 50)
    
    choice = input("Choose an option:\n1. Push to GitHub (for Railway)\n2. Show manual instructions\nEnter choice (1-2): ").strip()
    
    if choice == "1":
        setup_github_repo()
    elif choice == "2":
        print("\n📋 Manual Instructions:")
        print("1. Create a repository on GitHub")
        print("2. Run: git remote add origin https://github.com/username/repo-name.git")
        print("3. Run: git branch -M main")
        print("4. Run: git push -u origin main")
        print("5. Go to https://railway.app")
        print("6. Deploy from GitHub repository")
        print("7. Add GOOGLE_API_KEY environment variable")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
