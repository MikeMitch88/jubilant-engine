# 🔍 Troubleshooting 404 Error

## Understanding the Error

**404 Error means:** The server received your request but couldn't find the resource you're asking for.

Common causes:
1. ❌ Backend server not running
2. ❌ Wrong URL/endpoint being called
3. ❌ CORS issues (frontend can't reach backend)
4. ❌ Static files missing
5. ❌ Port mismatch

---

## 🎯 Quick Diagnosis

### Step 1: Check if Backend is Running

```bash
# Check if server is running on port 8000
curl http://localhost:8000/health

# Expected response:
{
  "status": "ok",
  "service": "Codebase Genius API",
  "jac_service": "operational"
}
```

**If it fails:**
```bash
# Start the backend server
cd /mnt/user-data/outputs/codebase-genius-fixed
python3 server.py
```

---

### Step 2: Check Available Endpoints

Your API has these endpoints:

```
GET  /                      # Root
GET  /health               # Health check
POST /analyze              # Analyze repository
GET  /history              # Analysis history
GET  /download/{repo_name} # Download docs
GET  /view/{repo_name}     # View docs content
```

**Test each one:**
```bash
# Root
curl http://localhost:8000/

# Health
curl http://localhost:8000/health

# History
curl http://localhost:8000/history

# Analyze (POST)
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"repo_url":"https://github.com/octocat/Hello-World"}'
```

---

### Step 3: Check Streamlit Configuration

**File:** `app.py` (line 173)
```python
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")
```

**This means:**
- Streamlit expects the backend at `http://localhost:8000`
- You can override with environment variable: `export API_URL=http://localhost:8000`

---

## 🐛 Common 404 Scenarios

### Scenario 1: Backend Not Running
**Symptom:** All requests return 404
**Solution:**
```bash
cd /mnt/user-data/outputs/codebase-genius-fixed
python3 server.py
# Or
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

---

### Scenario 2: Wrong Port
**Symptom:** Connection refused or 404
**Check ports:**
```bash
# See what's running on port 8000
lsof -i :8000
# Or
netstat -tuln | grep 8000
```

**Solution:**
- Make sure backend is on port 8000
- Make sure Streamlit is NOT on port 8000 (it should be 8501)

---

### Scenario 3: Streamlit Looking for Static Files
**Symptom:** 404 in browser console for `.js` or `.css` files
**This is normal** - Streamlit handles its own assets
**If you see:** `Failed to load resource: the server responded with a status of 404 ()`

Check browser console to see WHICH resource failed:
1. Press F12 (Developer Tools)
2. Go to Network tab
3. Reload page
4. Look for red/failed requests

---

### Scenario 4: CORS Issues
**Symptom:** 404 or CORS errors when Streamlit calls backend
**Current configuration in server.py:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ This allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**This should work!** But if it doesn't:
```python
# Try specific origins
allow_origins=[
    "http://localhost:8501",
    "http://127.0.0.1:8501"
]
```

---

### Scenario 5: Endpoint Path Mismatch
**Check what URL is being called:**

In browser console (F12), look for failed requests like:
- ❌ `http://localhost:8000/api/analyze` (wrong - no `/api/` prefix)
- ✅ `http://localhost:8000/analyze` (correct)

---

## 🔧 Complete Startup Sequence

### Terminal 1: Start Backend
```bash
cd /mnt/user-data/outputs/codebase-genius-fixed
python3 server.py
```

**Expected output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2: Start Streamlit
```bash
cd /mnt/user-data/outputs/codebase-genius-fixed
streamlit run app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Terminal 3: Test Backend
```bash
curl http://localhost:8000/health
```

**Expected:**
```json
{
  "status": "ok",
  "service": "Codebase Genius API",
  "note": "Health check running in API mode"
}
```

---

## 🔍 Detailed Debugging Steps

### 1. Check Exact Error in Browser

Open browser console (F12) and look for the failed request:

**Example errors:**
```
GET http://localhost:8000/favicon.ico 404 (Not Found)
→ Normal, backend doesn't serve favicon

GET http://localhost:8000/static/css/main.css 404 (Not Found)
→ Problem: Backend doesn't serve static files

POST http://localhost:8000/analyze 404 (Not Found)
→ Problem: Endpoint doesn't exist or server not running
```

### 2. Check Server Logs

When you make a request, check the terminal where `python3 server.py` is running.

**Good log:**
```
INFO:     127.0.0.1:xxxxx - "GET /health HTTP/1.1" 200 OK
```

**Bad log:**
```
INFO:     127.0.0.1:xxxxx - "GET /wrong-endpoint HTTP/1.1" 404 Not Found
```

### 3. Verify Streamlit Connection

In `app.py`, add debug output:

```python
# Around line 179
st.write(f"🔗 API URL: {API_BASE_URL}")
try:
    response = requests.get(f"{API_BASE_URL}/health", timeout=5)
    st.write(f"✅ Response Status: {response.status_code}")
    st.write(f"📝 Response: {response.json()}")
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
```

---

## 🛠️ Quick Fixes

### Fix 1: Restart Everything
```bash
# Kill any existing processes
pkill -f "python3 server.py"
pkill -f "streamlit run"

# Start fresh
cd /mnt/user-data/outputs/codebase-genius-fixed
python3 server.py &
sleep 3
streamlit run app.py
```

### Fix 2: Check Ports
```bash
# Make sure port 8000 is free
lsof -ti:8000 | xargs kill -9

# Make sure port 8501 is free  
lsof -ti:8501 | xargs kill -9

# Now start services
python3 server.py &
streamlit run app.py
```

### Fix 3: Use Explicit Ports
```bash
# Backend on 8000
uvicorn server:app --host 0.0.0.0 --port 8000

# Frontend on 8501
streamlit run app.py --server.port 8501
```

### Fix 4: Check Network Access
```bash
# Test localhost
curl http://localhost:8000/health

# Test 127.0.0.1
curl http://127.0.0.1:8000/health

# Test 0.0.0.0
curl http://0.0.0.0:8000/health
```

---

## 📋 Verification Checklist

Run through this checklist:

- [ ] Backend server is running (`python3 server.py`)
- [ ] Server shows "Uvicorn running on http://0.0.0.0:8000"
- [ ] Can access `http://localhost:8000/health` in browser
- [ ] Streamlit is running (`streamlit run app.py`)
- [ ] Streamlit shows on `http://localhost:8501`
- [ ] No error messages in backend terminal
- [ ] No error messages in Streamlit terminal
- [ ] Browser console shows the specific 404 URL
- [ ] Ports 8000 and 8501 are not used by other processes

---

## 🎯 Most Likely Issues

### Issue #1: Backend Not Running (90% of cases)
**Solution:** `python3 server.py`

### Issue #2: Port Conflict
**Solution:** Kill other processes on port 8000

### Issue #3: Wrong API URL
**Solution:** Check `API_BASE_URL` in app.py matches where server is running

### Issue #4: Missing Static Files (Normal)
**Solution:** Ignore 404s for favicon.ico or other static assets

---

## 💡 Next Steps

1. **Start the backend:** `python3 server.py`
2. **Test it:** `curl http://localhost:8000/health`
3. **Start Streamlit:** `streamlit run app.py`
4. **Open browser:** http://localhost:8501
5. **Check console:** F12 → Network tab → Look for failed requests
6. **Report:** Share the exact URL that's returning 404

---

## 📞 Still Having Issues?

Provide this information:
1. Output of `curl http://localhost:8000/health`
2. Browser console error (exact URL that's 404)
3. Backend server terminal output
4. Streamlit terminal output
5. Which OS/environment you're using

This will help pinpoint the exact issue! 🎯
