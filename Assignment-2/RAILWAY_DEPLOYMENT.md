# Railway Deployment Guide - Codebase Genius

Complete guide to deploying your Codebase Genius application on Railway.

## Why Railway?

Railway is **perfect** for your application because it:
- ✅ Supports long-running processes (10+ minute analysis jobs)
- ✅ Provides persistent file storage (your `outputs/` directory)
- ✅ Has no serverless limitations
- ✅ Supports subprocess execution (git, jac, python)
- ✅ Offers generous free tier ($5/month credit)
- ✅ **No cold starts** like Render's free tier
- ✅ Automatic HTTPS and custom domains

## Prerequisites

1. **GitHub Account** with your repository
2. **Railway Account** - Sign up at https://railway.app (use GitHub login)
3. **Repository**: `MikeMitch88/jubilant-engine`

## Quick Deployment Steps

### Step 1: Sign Up for Railway

1. Go to https://railway.app
2. Click "Login" and sign in with GitHub
3. Authorize Railway to access your repositories

### Step 2: Deploy Backend API

1. From Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose `MikeMitch88/jubilant-engine`
4. Railway will auto-detect the Python project

#### Configure Backend Service:

1. **Root Directory**:
   - Click "Settings" tab
   - Set "Root Directory" to: `Assignment-2`

2. **Build Command** (if not auto-detected):
   ```bash
   pip install --upgrade pip && pip install -r requirements-production.txt
   ```

3. **Start Command**:
   ```bash
   uvicorn server:app --host 0.0.0.0 --port $PORT
   ```

4. **Environment Variables**:
   - Railway automatically provides `PORT` - no need to set it
   - Optional: Add `PYTHON_VERSION=3.12` if needed

5. **Generate Domain**:
   - Go to "Settings" → "Networking"
   - Click "Generate Domain"
   - Copy the URL (e.g., `codebase-genius-api.up.railway.app`)

### Step 3: Deploy Frontend (Optional - can keep on Render)

You have two options:

#### Option A: Keep Frontend on Render
Just update the `API_URL` environment variable in your Render frontend service to point to your new Railway backend URL.

#### Option B: Move Frontend to Railway Too

1. Click **"New"** → **"Service"** → **"GitHub Repo"**
2. Select the same repository
3. Configure:
   - **Root Directory**: `Assignment-2`
   - **Start Command**:
     ```bash
     streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
     ```
   - **Environment Variables**:
     - `API_URL` = Your Railway backend URL (from Step 2)
     - `PORT` = Railway provides this automatically

4. Generate domain for frontend

### Step 4: Update Frontend API URL

If keeping frontend on Render:

1. Go to your Render dashboard
2. Navigate to `codebase-genius-ui` service
3. Go to "Environment"
4. Update `API_URL` to your Railway backend URL
5. Click "Save Changes" (triggers redeploy)

If moved frontend to Railway:

1. Already configured in Step 3 environment variables

### Step 5: Test Your Deployment

1. Visit your frontend URL
2. The backend status should show: **✅ Backend: Online**
3. Try analyzing a small repository to test the full flow

## Configuration Files Created

The following files have been added to your repository:

- **`railway.json`**: Railway-specific configuration
- **`Procfile.railway`**: Process definitions for Railway
- **`requirements-production.txt`**: Production dependencies (already exists)

## Railway Advantages Over Render

| Feature | Railway | Render (Free) |
|---------|---------|---------------|
| Cold Starts | ❌ None | ✅ Yes (15 min) |
| Persistent Storage | ✅ Yes | ✅ Yes |
| Execution Time | ✅ Unlimited | ✅ Unlimited |
| Monthly Cost | $5 credit free | $0 (with cold starts) |
| Build Speed | ✅ Fast | ⚠️ Medium |
| Auto Sleep | ❌ No | ✅ Yes |

## Environment Variables Reference

### Backend (FastAPI)
- `PORT` - Auto-provided by Railway
- `PYTHON_VERSION` - Optional: `3.12` (usually auto-detected)

### Frontend (Streamlit)
- `PORT` - Auto-provided by Railway
- `API_URL` - **Required**: Your Railway backend URL

## Troubleshooting

### Build Fails with "requirements.txt not found"
**Solution**: Make sure "Root Directory" is set to `Assignment-2` in Settings

### Health Check Fails
**Solution**:
- Verify the health check path is set to `/health`
- Check backend logs for errors
- Ensure port binding is using `$PORT` variable

### "Module not found" errors
**Solution**:
- Verify `requirements-production.txt` includes all dependencies
- Check build logs for pip installation errors
- May need to add system dependencies in railway.json

### Frontend shows "Backend: Offline"
**Solution**:
- Verify `API_URL` environment variable is set correctly
- Check backend service is running (green status in Railway)
- Test backend URL directly: `https://your-backend.up.railway.app/health`
- Ensure backend URL doesn't have trailing slash

### JacLang Service Issue
**Solution**:
- Ensure `jaclang==0.7.15` is in requirements-production.txt
- Check if JacLang requires additional system dependencies
- Review backend logs for specific JacLang errors

## Monitoring & Logs

### View Logs
1. Click on your service in Railway dashboard
2. Go to "Deployments" tab
3. Click on the active deployment
4. View real-time logs

### Metrics
1. Click "Metrics" tab to see:
   - CPU usage
   - Memory usage
   - Network traffic
   - Request counts

### Alerts
Railway can send alerts via:
- Email
- Slack
- Discord
- Webhooks

Configure in Project Settings → Notifications

## Cost Management

### Free Tier Usage
- $5 credit per month
- Monitor usage in Dashboard → Usage
- Typical usage for your app: ~$3-8/month depending on traffic

### Tips to Reduce Costs
1. Use `requirements-production.txt` (no dev dependencies)
2. Optimize Docker image size
3. Monitor memory usage
4. Scale down if not using heavily

## Scaling

### Vertical Scaling (More Resources)
1. Go to Service Settings
2. Adjust resources:
   - Memory: 512MB - 32GB
   - CPU: 1-32 vCPUs

### Horizontal Scaling (Multiple Instances)
Railway Pro plan supports replicas for high availability

## Custom Domains

### Add Your Domain
1. Go to Service → Settings → Networking
2. Click "Custom Domain"
3. Add your domain (e.g., `api.yourdomain.com`)
4. Update DNS records as instructed
5. Railway provides automatic SSL certificates

## Backup Strategy

### Code
- Backed up in GitHub automatically

### Generated Documentation (outputs/)
- Railway provides persistent storage
- Consider setting up periodic backups to:
  - AWS S3
  - Google Cloud Storage
  - GitHub (commit outputs periodically)

## Migration from Render

If you want to completely migrate from Render:

1. ✅ Deploy backend on Railway (Step 2)
2. ✅ Deploy frontend on Railway (Step 3 Option B)
3. Test thoroughly on Railway
4. Update any external links
5. Delete Render services (or keep as backup)

## Support

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **Railway Status**: https://status.railway.app

## Next Steps

1. ✅ Deploy backend to Railway
2. ✅ Update frontend API_URL
3. ✅ Test the application
4. Consider adding:
   - Database for storing analysis history
   - Redis for caching
   - S3-compatible storage for outputs
   - CI/CD with GitHub Actions

---

**Need Help?** Check Railway docs or reach out on their Discord community.
