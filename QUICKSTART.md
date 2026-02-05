# 🚀 Quick Start Guide

Get your TataCliq scraper running in 5 minutes!

## Option 1: Run Locally (Fastest for Testing)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
streamlit run app.py
```

### Step 3: Open Browser
Your browser should automatically open to `http://localhost:8501`

### Step 4: Upload and Scrape
1. Use the provided `sample_input.xlsx` or create your own
2. Click "Upload Excel file"
3. Click "🚀 Start Scraping"
4. Download results when complete

## Option 2: Deploy to Streamlit Cloud (Best for Sharing)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/tatacliq-scraper.git
git push -u origin main
```

### Step 2: Deploy
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository and `app.py`
5. Click "Deploy"

### Step 3: Share
Share your app URL with anyone who needs it!

## Creating Input Files

### Format 1: Using URLs
```
| s.no | url                                                                    |
|------|------------------------------------------------------------------------|
| 1    | https://www.tatacliq.com/product-name/p-mp000000026178350             |
```

### Format 2: Using IDs
```
| s.no | id                    |
|------|-----------------------|
| 1    | mp000000026178350     |
```

## Tips for Success

✅ **Start Small**: Test with 5-10 products first
✅ **Use 4-8 Workers**: Good balance of speed and stability
✅ **Check Logs**: Monitor the progress log for errors
✅ **Valid URLs**: Ensure all URLs are from TataCliq.com

## Common Issues

### "No data scraped"
- Verify URLs/IDs are correct
- Check internet connection
- Try fewer workers

### Rate limiting
- Reduce concurrent workers to 4
- Wait a few minutes between large batches

### Missing fields
- Normal - not all products have all data
- Check progress log for specific errors

## Next Steps

📖 Read the full [README.md](README.md) for detailed documentation
🚀 See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment guide
💡 Customize `app.py` for your specific needs

---

**Need Help?** Open an issue on GitHub or check the Streamlit forums.

Happy Scraping! 🎉
