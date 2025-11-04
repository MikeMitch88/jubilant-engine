# 🚀 Quick Start Guide - Codebase Genius

Get up and running with Codebase Genius in 5 minutes!

---

## ⚡ Super Quick Start

```bash
# 1. Clone and setup
cd codebase-genius
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Run the system
./start.sh
# Select option 1 (Full system)

# 3. Open browser
# Streamlit will auto-open at http://localhost:8501
```

---

## 📝 Step-by-Step Guide

### Step 1: Environment Setup (2 min)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Verify installation**:
```bash
python test_setup.py
```

### Step 2: Start the System (1 min)

**Option A - Use startup script** (Recommended):
```bash
./start.sh
```
Then select option 1.

**Option B - Manual start**:

Terminal 1 (API):
```bash
uvicorn server:app --reload --port 8000
```

Terminal 2 (UI):
```bash
streamlit run app.py
```

### Step 3: Analyze Your First Repository (2 min)

1. Open browser to `http://localhost:8501`
2. Enter a repository URL, e.g.: `https://github.com/pallets/flask`
3. Click "🔍 Analyze Repository"
4. Watch the progress messages
5. View or download the documentation when complete!

---

## 🎯 Try These Example Repositories

Start with these small, well-structured repos:

**Small Repos (Fast - 1-2 min)**:
```
https://github.com/psf/requests
https://github.com/pallets/click
```

**Medium Repos (Moderate - 3-5 min)**:
```
https://github.com/pallets/flask
https://github.com/django/django
```

---

## 🔍 What to Expect

### Analysis Progress
You'll see messages like:
1. 🔍 Initializing Code Genius supervisor...
2. 📥 Cloning repository...
3. 🗺️ Mapping file structure...
4. 🔬 Analyzing code with AST parser...
5. 🧬 Building Code Context Graph...
6. 📝 Generating documentation...
7. ✨ Finalizing output...

### Generated Documentation
The system creates a markdown file with:
- 📖 Project overview and statistics
- 📁 File structure tree
- 🏗️ Code structure breakdown
- 🔗 Relationship diagrams (Mermaid)
- 📚 API reference tables

### Output Location
```
outputs/
└── repository-name/
    └── documentation.md
```

---

## 🎨 Using the UI

### Main Screen
- **Input**: Enter GitHub URL
- **Button**: "🔍 Analyze Repository"
- **Progress**: Real-time status updates
- **Results**: View or download documentation

### Sidebar
- **System Status**: Backend health indicator
- **Recent Analyses**: Quick access to history
- **New Analysis**: Start fresh analysis

### After Analysis
- **👁️ View Documentation**: Preview in browser
- **📥 Download Markdown**: Save to disk
- **⬅️ Back**: Return to analysis screen

---

## 🛠️ Common Commands

### Check System Health
```bash
curl http://localhost:8000/health
```

### Test API Directly
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"repo_url":"https://github.com/pallets/flask"}'
```

### View History
```bash
curl http://localhost:8000/history
```

### Download Documentation
```bash
curl http://localhost:8000/download/flask -o flask_docs.md
```

---

## 🐛 Quick Troubleshooting

### "Backend Offline" in UI
```bash
# Check if API is running
curl http://localhost:8000/health

# If not, start it
uvicorn server:app --reload --port 8000
```

### "Module not found" errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### "Git clone failed"
- Ensure repository URL is correct and public
- Check your internet connection
- Verify Git is installed: `git --version`

### Analysis seems stuck
- Check terminal for error messages
- Large repos can take 5-10 minutes
- Try a smaller repo first

---

## 📊 API Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/analyze` | POST | Start analysis |
| `/history` | GET | List analyses |
| `/download/{name}` | GET | Download docs |
| `/view/{name}` | GET | View content |

---

## 💡 Pro Tips

1. **Start Small**: Test with small repos (< 50 files) first
2. **Check Logs**: Terminal shows detailed progress
3. **Use History**: Access previous analyses from sidebar
4. **Download Early**: Save documentation before starting new analysis
5. **Keep It Running**: Leave API running between analyses

---

## 🎓 Next Steps

Once comfortable with basics:

1. **Read ARCHITECTURE.md** - Understand the multi-agent system
2. **Explore main.jac** - See JacLang walker implementation
3. **Customize Output** - Modify doc_generator.py templates
4. **Add Features** - Integrate LLM for enhanced summaries
5. **Scale Up** - Analyze larger, more complex repositories

---

## 🆘 Need Help?

1. Run diagnostic: `python test_setup.py`
2. Check README.md for detailed docs
3. Review terminal logs for errors
4. Ensure all dependencies installed
5. Verify Git and Python versions

---

## ✨ Success Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Test script passed (`python test_setup.py`)
- [ ] API server running (port 8000)
- [ ] Streamlit UI running (port 8501)
- [ ] First repository analyzed
- [ ] Documentation generated and viewed
- [ ] Downloaded markdown file

---

**Ready to analyze codebases like a genius? Let's go! 🚀**

For detailed information, see [README.md](README.md) and [ARCHITECTURE.md](ARCHITECTURE.md).
