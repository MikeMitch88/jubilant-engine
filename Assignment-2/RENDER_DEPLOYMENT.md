# 🚀 Deploying Codebase Genius to Render

This guide will help you deploy your Codebase Genius application to Render with both backend and frontend services.

## 📋 Prerequisites

- [Render account](https://render.com/) (free tier works!)
- Git repository (GitHub, GitLab, or Bitbucket)
- Your code pushed to the repository

## 🎯 Deployment Strategy

We'll deploy **two separate services**:
1. **Backend API** (FastAPI) - Will be assigned a URL like `https://codebase-genius-api.onrender.com`
2. **Frontend UI** (Streamlit) - Will be assigned a URL like `https://codebase-genius-ui.onrender.com`

---

## 🚀 Option 1: Deploy Using Blueprint (Recommended)

This method uses the `render.yaml` file to automatically create both services.

### Step 1: Push Your Code to GitHub

```bash
# If not already a git repo
git init
git add .
git commit -m "Initial commit for Render deployment"

# Add your GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### Step 2: Connect to Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub/GitLab repository
4. Select your repository: `jubilant-engine` or your specific repo
5. Set the **Root Directory** to: `Assignment-2`
6. Render will automatically detect `render.yaml`
7. Click **"Apply"**

### Step 3: Configure Environment Variables

After deployment starts:

1. **Backend Service** (codebase-genius-api):
   - No additional env vars needed initially
   - Note the deployed URL (e.g., `https://codebase-genius-api.onrender.com`)

2. **Frontend Service** (codebase-genius-ui):
   - Go to service settings → Environment
   - Add environment variable:
     - **Key**: `API_URL`
     - **Value**: `https://codebase-genius-api.onrender.com` (use your actual backend URL)
   - Click **"Save Changes"**
   - The service will automatically redeploy

### Step 4: Wait for Deployment

- Backend build typically takes 3-5 minutes
- Frontend build typically takes 3-5 minutes
- Watch the logs for any errors

### Step 5: Test Your Application

1. Open the Frontend URL (e.g., `https://codebase-genius-ui.onrender.com`)
2. Check that "Backend: Online" appears in the sidebar
3. Try analyzing a small repository like `https://github.com/pallets/flask`

---

## 🛠️ Option 2: Deploy Services Manually

If you prefer to create services one by one:

### Deploy Backend (FastAPI)

1. Click **"New +"** → **"Web Service"**
2. Connect your repository
3. Configure:
   - **Name**: `codebase-genius-api`
   - **Root Directory**: `Assignment-2`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `./start_backend.sh`
   - **Plan**: `Free`
4. Add environment variable:
   - `PYTHON_VERSION` = `3.12.0`
5. Click **"Create Web Service"**
6. **IMPORTANT**: Copy the deployed URL (you'll need it for the frontend)

### Deploy Frontend (Streamlit)

1. Click **"New +"** → **"Web Service"**
2. Connect your repository
3. Configure:
   - **Name**: `codebase-genius-ui`
   - **Root Directory**: `Assignment-2`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `./start_frontend.sh`
   - **Plan**: `Free`
4. Add environment variables:
   - `PYTHON_VERSION` = `3.12.0`
   - `API_URL` = `https://YOUR-BACKEND-URL.onrender.com` (from step 6 above)
5. Click **"Create Web Service"**

---

## ⚙️ Configuration Files Explained

### render.yaml
Blueprint configuration that defines both services and their settings.

### start_backend.sh
Startup script for the FastAPI backend service. Creates necessary directories and starts uvicorn.

### start_frontend.sh
Startup script for the Streamlit frontend. Configures Streamlit for production and connects to backend.

### requirements.txt
Python dependencies needed for both services.

---

## 🐛 Troubleshooting

### Build Fails with "Module not found"

**Solution**: Check that all dependencies are in `requirements.txt`

```bash
# Locally test the build
pip install -r requirements.txt
```

### Frontend Shows "Backend: Offline"

**Cause**: Frontend can't reach the backend

**Solution**:
1. Verify backend is deployed and running (check Render dashboard)
2. Check backend URL in logs: https://YOUR-BACKEND.onrender.com/health
3. Verify `API_URL` environment variable in frontend service matches backend URL exactly
4. Redeploy frontend after setting API_URL

### Backend Health Check Fails

**Cause**: Backend taking too long to start or crashing

**Solution**:
1. Check backend logs in Render dashboard
2. Look for Python errors or missing dependencies
3. Verify the health check endpoint works: `/health`
4. Increase health check timeout if needed (in Service settings)

### "Repository Analysis Times Out"

**Cause**: Free tier Render has limited resources

**Solution**:
1. Try analyzing smaller repositories first
2. Consider upgrading to a paid plan for more resources
3. Increase timeout in `server.py` if needed (currently 600 seconds)

### Streamlit Shows Blank Page

**Cause**: CORS or configuration issue

**Solution**:
1. Check that `start_frontend.sh` has correct Streamlit flags
2. Verify logs for any Streamlit errors
3. Make sure `--server.headless=true` is set

---

## 📊 Free Tier Limitations

Render's free tier includes:
- ✅ 750 hours/month per service
- ✅ Automatic HTTPS
- ✅ Custom domains supported
- ⚠️ Services spin down after 15 minutes of inactivity
- ⚠️ Cold start takes 30-60 seconds when inactive
- ⚠️ Limited to 512 MB RAM

**Note**: First request after inactivity will be slow. Consider:
- Using a paid plan ($7/month) for always-on services
- Using a service like UptimeRobot to ping your app every 14 minutes

---

## 🔒 Security Considerations

### For Production Use:

1. **Add CORS restrictions** in `server.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-url.onrender.com"],  # Restrict to your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. **Add rate limiting** (install `slowapi`):
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

3. **Add authentication** for sensitive operations

4. **Set up environment variables** for secrets (never commit them!)

---

## 📈 Monitoring Your Deployment

### Check Service Health

- Backend: `https://YOUR-BACKEND.onrender.com/health`
- Backend API Docs: `https://YOUR-BACKEND.onrender.com/docs`
- Frontend: `https://YOUR-FRONTEND.onrender.com`

### View Logs

1. Go to Render Dashboard
2. Click on your service
3. Click "Logs" tab
4. Real-time logs will appear

### Metrics

In Render Dashboard:
- CPU usage
- Memory usage
- Request count
- Response times

---

## 🔄 Updating Your Deployment

### Auto-Deploy (Recommended)

When `autoDeploy: true` is set in `render.yaml`:
1. Push changes to your GitHub repository
2. Render automatically detects changes
3. Rebuild and redeploy happens automatically

### Manual Deploy

1. Go to Render Dashboard
2. Select your service
3. Click "Manual Deploy" → "Deploy latest commit"

---

## 💰 Cost Optimization

**Free Tier**:
- Use for development and testing
- Services sleep after inactivity
- Best for low-traffic demos

**Starter Plan ($7/month per service)**:
- Always-on (no sleeping)
- Better performance
- Priority support
- Good for production with moderate traffic

---

## ✅ Deployment Checklist

Before deploying:
- [ ] Code is pushed to GitHub/GitLab
- [ ] `requirements.txt` has all dependencies
- [ ] `render.yaml` is configured correctly
- [ ] `.gitignore` excludes `venv/`, `outputs/`, `__pycache__/`
- [ ] Startup scripts are executable (`chmod +x *.sh`)

After deploying backend:
- [ ] Backend health endpoint works
- [ ] Note the backend URL

After deploying frontend:
- [ ] Set `API_URL` environment variable to backend URL
- [ ] Frontend shows "Backend: Online"
- [ ] Test analyzing a repository

---

## 🎉 Success!

Once deployed, you'll have:
- 🚀 **Backend API**: https://codebase-genius-api.onrender.com
- 🎨 **Frontend UI**: https://codebase-genius-ui.onrender.com
- 📚 **API Docs**: https://codebase-genius-api.onrender.com/docs

Share your Frontend URL with others to let them analyze repositories!

---

## 📞 Support

If you encounter issues:
1. Check Render's [status page](https://status.render.com/)
2. Review [Render docs](https://render.com/docs)
3. Check service logs in Render Dashboard
4. Review this troubleshooting guide

---

## 🔗 Useful Links

- [Render Dashboard](https://dashboard.render.com/)
- [Render Documentation](https://render.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [JacLang Documentation](https://www.jac-lang.org/)

---

**Happy Deploying! 🚀**
