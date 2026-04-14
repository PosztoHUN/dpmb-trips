# Deploying to GitHub + Railway

This guide explains how to deploy your DPMB Public Transport website to GitHub and run it on Railway (a modern deployment platform).

## Why Railway?

✅ **Free tier available** - Deploy for free  
✅ **Easy GitHub integration** - Auto-deploy on push  
✅ **Node.js support** - Perfect for our app  
✅ **Environment variables** - Store logs path securely  
✅ **Health checks** - Automatic monitoring  
✅ **Web dashboard** - Easy management  
✅ **Custom domain** - Use your own domain (optional)  

---

## Prerequisites

- GitHub account (free at https://github.com)
- Railway account (free at https://railway.app)
- Git installed on your computer
- Your trip data ready

---

## Step 1: Set Up GitHub Repository

### 1.1 Create GitHub Repo

1. Go to https://github.com/new
2. Fill in details:
   - **Repository name:** `dpmb-trips` (or your choice)
   - **Description:** DPMB Public Transport Trip Tracking
   - **Visibility:** Public (anyone can see) or Private (only you)
   - **Initialize with:** Skip (we'll push existing code)
3. Click "Create repository"

### 1.2 Initialize Git Locally

Open PowerShell in `g:\Suli\dpmb-trips` and run:

```powershell
# Initialize git (if not already done)
git init

# Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/dpmb-trips.git

# Set branch to main
git branch -M main

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: DPMB public transport tracker"

# Push to GitHub
git push -u origin main
```

**Replace** `YOUR_USERNAME` with your GitHub username.

### 1.3 Verify on GitHub

1. Visit: `https://github.com/YOUR_USERNAME/dpmb-trips`
2. You should see your files uploaded

---

## Step 2: Prepare Application for Railway

### 2.1 Files Already Created

These files are ready for Railway:

```
✓ Dockerfile - Container configuration
✓ Procfile - Process file for Railway
✓ .github/workflows/deploy.yml - Auto-deploy on push
✓ railway.json - Railway configuration
✓ .gitignore - Excludes unwanted files
```

### 2.2 Set Up Environment Variables

Create `.env` file (Railway will read this):

```bash
NODE_ENV=production
PORT=3001
CORS_ORIGIN=*
LOGS_DIR=/data/logs
```

**But don't commit this to GitHub!** It's in `.gitignore` for security.

---

## Step 3: Deploy to Railway

### 3.1 Connect GitHub to Railway

1. Go to https://railway.app
2. Sign up (free account)
3. Click "Create New Project"
4. Select "Deploy from GitHub"
5. **Authorize Railway** to access your GitHub
6. Find and select `dpmb-trips` repository
7. Click "Import"

### 3.2 Configure Railway Project

After importing, Railway will show project settings:

1. **Builder:** Select "Nixpacks" (default)
2. **Start Command:** Should auto-detect from Procfile
3. **Port:** 3001 (already set in code)

### 3.3 Set Environment Variables in Railway

1. Go to your Railway project settings
2. Find "Variables" section
3. Add these variables:

```
NODE_ENV = production
PORT = 3001
CORS_ORIGIN = *
LOGS_DIR = /data/logs
```

### 3.4 Deploy

Click "Deploy" button. Railway will:
1. Build your app
2. Install dependencies
3. Start the server
4. Assign you a URL

**Wait 2-3 minutes for deployment to complete.**

---

## Step 4: Upload Trip Data to Railway

Railway needs access to your trip log files. There are several options:

### Option A: Use Railway File System (Recommended)

1. After deployment, use Railway's file browser
2. Navigate to `/app` directory
3. Create `/data/logs` folder
4. Upload your `.txt` files from `G:\Suli\DPMB-bot\logs\2026-04-14\`

### Option B: Mount External Storage

Contact Railway support for persistent storage options.

### Option C: GitHub LFS

For large files, use Git LFS to store trip data.

---

## Step 5: Verify Deployment

### 5.1 Get Your URL

In Railway dashboard:
1. Click your project
2. Find "Deployments" section
3. Copy the URL (looks like: `https://xyz-production.up.railway.app`)

### 5.2 Test the App

1. Visit: `https://xyz-production.up.railway.app`
2. You should see the website
3. Test endpoints:
   - `https://xyz-production.up.railway.app/api/lines`
   - `https://xyz-production.up.railway.app/api/stats`

---

## Step 6: Auto-Deploy on Updates

### 6.1 How It Works

Once configured:
- Push code to `main` branch
- GitHub Actions runs tests
- If tests pass, Railway auto-deploys

### 6.2 Deploy New Code

```powershell
# Make changes to files
# Example: edit frontend/app.js

# Commit changes
git add .
git commit -m "Update: improved UI styling"

# Push to GitHub
git push origin main
```

**GitHub Actions will automatically:**
1. Test your code
2. Deploy to Railway
3. Update the live website

---

## Step 7: Configure Custom Domain (Optional)

### 7.1 Add Your Domain

In Railway dashboard:
1. Go to "Settings"
2. Find "Domain" section
3. Add custom domain (e.g., `dpmb.yourdomain.com`)
4. Update DNS settings with your domain provider

### 7.2 Example DNS Setup

Contact your domain registrar and point to Railway's nameservers.

---

## Troubleshooting

### App Won't Deploy

**Check:**
- All required files exist (server.js, package.json)
- No syntax errors in code
- package.json has correct "start" script

**Fix:**
```powershell
# Check for errors locally
cd backend
npm install
npm start

# Fix any issues, then push
git add .
git commit -m "Fix: production deployment errors"
git push origin main
```

### No Data Loading

**Problem:** Website shows but no trips display.

**Solution:**
1. Upload trip files to `/data/logs` via Railway file browser
2. Restart the app in Railway
3. Check health endpoint: `/health`

**Or use environment variable:**
```
LOGS_DIR = /path/to/your/uploaded/logs
```

### 502 Bad Gateway

**Problem:** Website returns error.

**Solution:**
1. Check Railway logs (Deployments → View Logs)
2. Verify port is 3001
3. Check package.json "start" script

### App Crashes After Deploy

**Check:**
1. Railway logs for error messages
2. Verify dependencies installed: Check `package.json`
3. Make sure trip data directory exists: `/data/logs`

---

## Monitoring Your App

### Check Health

```bash
curl https://YOUR_RAILWAY_URL/health
```

Response shows if data is loaded.

### View Logs

In Railway dashboard:
1. Click project
2. Click "Deployments"
3. Select latest deployment
4. Click "View Logs"

### Get Usage Stats

```bash
curl https://YOUR_RAILWAY_URL/api/stats
```

Shows total lines and trips.

---

## Update Log Files

### Refresh Data on Railway

1. SSH into Railway container OR
2. Use file browser to replace trip files
3. Restart app (Railway → Deployments → Restart)

### Automate Updates

Create GitHub Action to sync logs daily:

```yaml
# .github/workflows/update-logs.yml
name: Update Trip Data
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Sync logs
        run: |
          # Copy new logs
          cp -r /network/logs/* backend/data/logs/
          git add .
          git commit -m "Update: daily trip data"
          git push
```

---

## Cost Breakdown

**Railway Pricing:**
- **Free tier:** $5/month credit (usually enough)
- **After free:** $0.000463 per hour (very cheap)
- **Storage:** Included in free tier
- **Bandwidth:** Included

**No fees for:**
- GitHub (free)
- Domain (optional, $10-15/year)

---

## Security Notes

### Protect Your Secret Data

1. Don't commit `.env` to GitHub (already in `.gitignore`)
2. Use Railway's secrets for sensitive info
3. Consider making repository private

### Railway Secrets

In Railway dashboard → Variables:
- Create separate vars for prod/dev
- Use for API keys, tokens
- Not exposed in code

---

## Maintenance

### Regular Tasks

- Check logs monthly for errors
- Update dependencies quarterly
- Monitor Railway usage
- Backup trip data regularly

### Update Dependencies

```powershell
# Check for updates
npm outdated

# Update packages
npm update

# Commit and push
git add package*.json
git commit -m "Update: dependencies"
git push origin main
```

---

## Performance Tips

### Optimize Railway Usage

1. Set proper memory limits
2. Use caching headers
3. Enable compression
4. Minimize database queries (if using DB)

### Speed Up Deployment

1. Keep `.gitignore` clean
2. Remove unused files
3. Use lightweight dependencies
4. Minimize npm packages

---

## Scaling for Growth

### When You Need More Power

1. Upgrade Railway plan
2. Add database for persistence
3. Implement caching layer
4. Use CDN for static assets

### Example: Add PostgreSQL

```bash
# In Railway dashboard
1. Create database service
2. Connect to your app
3. Update code to use database
```

---

## Next Steps

1. **Create GitHub account** at https://github.com
2. **Create Railway account** at https://railway.app
3. **Follow steps above** to deploy
4. **Share your URL** with others
5. **Monitor** via Railway dashboard

---

## Getting Help

### Resources

- Railway Docs: https://docs.railway.app
- GitHub Help: https://docs.github.com
- This project's README: See README.md

### Common Commands

```powershell
# Check git status
git status

# View git history
git log --oneline

# Push to GitHub
git push origin main

# Pull latest
git pull origin main
```

---

## Summary

✅ Your app is now ready to deploy  
✅ Files configured for Railway  
✅ GitHub Actions set up for auto-deploy  
✅ Health checks included  

**Next action:** Push to GitHub and connect Railway!

---

**Need help?** Check the troubleshooting section or Railway's documentation.
