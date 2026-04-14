# Railway Deployment - 5 Minute Quick Start

## What is Railway?

Railway is a modern platform for deploying Node.js apps. Think of it as "Heroku but better" - simpler, cheaper, and easier.

---

## 5-Step Deployment

### Step 1: Push to GitHub (2 min)

```powershell
cd g:\Suli\dpmb-trips
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/dpmb-trips.git
git branch -M main
git push -u origin main
```

### Step 2: Sign Up to Railway (1 min)

1. Go to https://railway.app
2. Click "Sign Up"
3. Use GitHub to sign up (easiest)
4. Authorize Railway

### Step 3: Create Project (1 min)

1. Click "Create New Project"
2. Select "Deploy from GitHub"
3. Authorize GitHub
4. Select `dpmb-trips` repository
5. Click "Deploy"

### Step 4: Upload Trip Data (1 min)

Railway needs your trip `.txt` files:

1. In Railway dashboard → File Browser
2. Create folder: `/data/logs`
3. Upload your trip files from `G:\Suli\DPMB-bot\logs\2026-04-14\`

### Step 5: Get Your URL (0 min)

After deploy completes (~2 min):
1. Railway shows your URL: `https://xyz-production.up.railway.app`
2. Click it to open your live website!

---

## That's It!

Your website is now live on the internet! 🎉

You can share the URL with anyone and they can see all the tram/bus trips in Brno.

---

## Handy URLs

Once deployed:

| What | URL |
|------|-----|
| **Website** | https://xyz.up.railway.app |
| **All Lines** | https://xyz.up.railway.app/api/lines |
| **Line 1 Trips** | https://xyz.up.railway.app/api/lines/1/trips |
| **Statistics** | https://xyz.up.railway.app/api/stats |
| **Health Check** | https://xyz.up.railway.app/health |

---

## Auto-Deploy Updates

1. Make code changes locally
2. Commit: `git commit -am "My changes"`
3. Push: `git push origin main`
4. Railway auto-deploys! ✨

---

## Free Tier

- $5/month free credit
- Enough for this project
- Auto-restarts if needed
- Included: Storage, Bandwidth, Logs

---

## Troubleshooting

### Website won't load

**Check:**
1. Are trip files uploaded? (Check `/data/logs`)
2. Is app running? (Check Railway logs)

### No trips showing

**Fix:**
1. Upload trip `.txt` files to `/data/logs`
2. Restart app in Railway
3. Refresh browser

### Syntax errors

**Check:**
1. Test locally: `npm start`
2. Fix errors
3. Push to GitHub
4. Railway auto-redeploys

---

## Custom Domain (Optional)

Want `dpmb.yourdomain.com`?

1. Railway dashboard → Settings → Domain
2. Add your domain
3. Update DNS with your registrar
4. Done in 5 minutes

---

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Sign up to Railway
3. ✅ Deploy your app
4. ✅ Upload trip data
5. ✅ Share your URL!

**Current Status:** Ready to deploy! 🚀

See `GITHUB_RAILWAY_DEPLOYMENT.md` for detailed instructions.
