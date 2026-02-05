# 🚀 Deployment Guide for Streamlit Cloud

Follow these steps to deploy your TataCliq scraper to Streamlit Cloud:

## Prerequisites

1. A GitHub account
2. Git installed on your computer
3. The project files (already created)

## Step-by-Step Deployment

### 1. Create GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the "+" icon in the top right and select "New repository"
3. Name your repository (e.g., `tatacliq-scraper`)
4. Choose "Public" or "Private"
5. **Do NOT** initialize with README (we already have one)
6. Click "Create repository"

### 2. Push Code to GitHub

Open your terminal and run these commands in the project folder:

```bash
# Configure git (if first time)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Add all files
git add .

# Commit the files
git commit -m "Initial commit: TataCliq scraper"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/tatacliq-scraper.git

# Push to GitHub
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### 3. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign in with GitHub"
3. Authorize Streamlit Cloud to access your repositories
4. Click "New app"
5. Fill in the deployment form:
   - **Repository**: Select your `tatacliq-scraper` repository
   - **Branch**: `main`
   - **Main file path**: `app.py`
6. Click "Deploy!"

### 4. Wait for Deployment

- Streamlit Cloud will install dependencies from `requirements.txt`
- This usually takes 2-5 minutes
- Watch the deployment logs for any errors

### 5. Access Your App

Once deployed, you'll get a URL like:
```
https://YOUR_USERNAME-tatacliq-scraper-app-xxxxx.streamlit.app
```

Share this URL with anyone who needs to use the scraper!

## Updating Your App

After deployment, any changes you push to GitHub will automatically redeploy:

```bash
# Make your changes to the code
# Then:
git add .
git commit -m "Description of changes"
git push
```

Streamlit Cloud will detect the changes and redeploy automatically.

## Troubleshooting

### Issue: "Deployment failed"
- Check the deployment logs for specific errors
- Ensure all dependencies in `requirements.txt` are correct
- Verify that `app.py` has no syntax errors

### Issue: "File not found"
- Ensure the main file path is exactly `app.py`
- Check that all files were pushed to GitHub:
  ```bash
  git status
  ```

### Issue: "Import errors"
- Verify all packages in `requirements.txt` are spelled correctly
- Check that version numbers are compatible

### Issue: "App is slow"
- This is normal for the free tier
- Consider upgrading to Streamlit Cloud's paid tier for better performance
- Reduce the number of concurrent workers

## Advanced Configuration

### Custom Domain
1. Go to your app settings on Streamlit Cloud
2. Click "Settings" → "General"
3. Add your custom domain

### Environment Variables
If you need to add API keys or secrets:
1. Go to app settings
2. Click "Secrets"
3. Add your secrets in TOML format:
   ```toml
   api_key = "your-api-key"
   ```

### Resource Limits
Free tier limits:
- 1 GB RAM
- 1 CPU
- Apps sleep after inactivity

For higher limits, upgrade to the paid tier.

## Security Best Practices

1. **Never commit sensitive data**:
   - Use Streamlit secrets for API keys
   - Don't hardcode passwords or tokens
   - Use `.gitignore` to exclude sensitive files

2. **Update dependencies regularly**:
   ```bash
   pip install --upgrade streamlit pandas requests
   pip freeze > requirements.txt
   ```

3. **Monitor usage**:
   - Check Streamlit Cloud analytics
   - Watch for unusual activity

## Support

If you encounter issues:
- Check [Streamlit Community Forum](https://discuss.streamlit.io)
- Read [Streamlit Deployment Docs](https://docs.streamlit.io/streamlit-community-cloud)
- Open an issue on your GitHub repository

---

🎉 **Congratulations!** Your scraper is now live and accessible to anyone with the URL!
