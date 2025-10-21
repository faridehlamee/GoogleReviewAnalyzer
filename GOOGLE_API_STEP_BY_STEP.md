# 🔑 Google Places API Key - Step by Step Guide

## 📋 **Complete Step-by-Step Instructions**

### **Step 1: Go to Google Cloud Console**
1. Open your browser
2. Go to: **https://console.cloud.google.com/**
3. Sign in with your Google account

### **Step 2: Create a New Project**
1. Click on the **project dropdown** at the top of the page
2. Click **"New Project"**
3. Enter a project name (e.g., "Review Analyzer")
4. Click **"Create"**
5. Wait for the project to be created (usually takes a few seconds)

### **Step 3: Enable Billing** ⚠️ **IMPORTANT**
**Note**: Google requires billing to be enabled even for the free tier. Don't worry - you won't be charged for the first 1,000 requests per month.

1. In the left sidebar, click **"Billing"**
2. Click **"Link a billing account"**
3. Choose **"Create a new billing account"** or link an existing one
4. Fill in your billing information
5. **You won't be charged** for the free tier usage

### **Step 4: Enable Places API**
1. In the left sidebar, click **"APIs & Services"**
2. Click **"Library"**
3. In the search box, type **"Places API"**
4. Click on **"Places API"** from the results
5. Click **"Enable"**

### **Step 5: Create API Key**
1. In the left sidebar, click **"APIs & Services"**
2. Click **"Credentials"**
3. Click **"Create Credentials"** at the top
4. Select **"API Key"**
5. Your API key will be generated and displayed
6. **Copy the API key** (it looks like: `AIzaSyB...`)

### **Step 6: Secure Your API Key (Recommended)**
1. Click **"Restrict Key"** next to your API key
2. Under **"API restrictions"**, select **"Restrict key"**
3. Select **"Places API"** from the list
4. Click **"Save"**

### **Step 7: Add API Key to Your Project**
1. In your project folder, create a file called `.env`
2. Add this line to the file:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```
3. Replace `your_actual_api_key_here` with the API key you copied

## 🚀 **Quick Setup Script**

I've created a helper script to make this easier:

```bash
python setup_google_api.py
```

This script will:
- Guide you through the process
- Help you enter your API key
- Test if your API key is working
- Create/update your `.env` file

## 🧪 **Test Your Setup**

Once you have your API key set up:

```bash
# Test the system
python test_google_analyzer.py

# Test with real data
python utils.py
```

## 💰 **Cost Information**

### **Free Tier:**
- **1,000 requests per month** - FREE
- Perfect for testing and small projects

### **Paid Tier:**
- **$5 per 1,000 additional requests**
- Much cheaper than Yelp's $229/month minimum

### **Example Usage:**
- Analyzing 1 business = ~5-10 API calls
- Free tier = ~100-200 businesses per month
- Perfect for most use cases!

## ❓ **Common Questions**

### **Q: Do I really need billing enabled?**
A: Yes, Google requires billing even for free tier. You won't be charged for the first 1,000 requests per month.

### **Q: What if I exceed the free tier?**
A: You'll be charged $5 per 1,000 additional requests. You can set up billing alerts to monitor usage.

### **Q: Can I use this for commercial purposes?**
A: Yes, but check Google's terms of service for your specific use case.

### **Q: How do I find place IDs?**
A: Use the built-in search: `python utils.py` or find them in Google Maps URLs.

## 🔧 **Troubleshooting**

### **"API key not found"**
- Make sure you created `.env` file
- Check that `GOOGLE_API_KEY=your_key` is in the file
- Restart your terminal/command prompt

### **"Places API not enabled"**
- Go back to Google Cloud Console
- Enable Places API in the Library section

### **"Billing required"**
- Set up billing in Google Cloud Console
- Don't worry - you won't be charged for free tier usage

### **"No results found"**
- Check your search terms
- Try different location formats
- Verify your API key has proper permissions

## 🎉 **You're Ready!**

Once you have your API key set up:

1. **Test it**: `python test_google_analyzer.py`
2. **Find businesses**: `python utils.py`
3. **Analyze reviews**: `python main.py <place_id>`

Your Google Places Review Analyzer is ready to use! 🚀
