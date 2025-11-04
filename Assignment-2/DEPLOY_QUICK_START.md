# 🚀 Quick Deploy to Render - 5 Steps

## Step 1: Push to GitHub
```bash
cd /home/mike_mitch/code/jubilant-engine/Assignment-2
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

## Step 2: Create Blueprint on Render
1. Go to https://dashboard.render.com/
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Select root directory: `Assignment-2`
5. Click **"Apply"**

## Step 3: Get Backend URL
1. Wait for backend service to deploy (~3-5 mins)
2. Copy the backend URL (e.g., `https://codebase-genius-api-xxxx.onrender.com`)

## Step 4: Set Frontend Environment Variable
1. Click on **codebase-genius-ui** service
2. Go to **"Environment"** tab
3. Add variable:
   - Key: `API_URL`
   - Value: `https://codebase-genius-api-xxxx.onrender.com` (your backend URL)
4. Save (auto-redeploys)

## Step 5: Access Your App
1. Wait for frontend to redeploy (~2-3 mins)
2. Click the frontend URL
3. Verify "Backend: Online" in sidebar
4. Start analyzing repositories!

---

## 📝 Important Notes

- **Free tier services sleep after 15 min** - First request takes 30-60 sec to wake up
- **Both services needed** - Backend AND Frontend must be running
- **Set API_URL correctly** - Frontend won't work without it

---

## 🐛 Quick Troubleshooting

**"Backend: Offline"** → Check API_URL environment variable matches backend URL

**Build failed** → Check logs in Render dashboard for specific error

**Service not starting** → Verify `requirements.txt` has all dependencies

---

For detailed guide, see [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)
