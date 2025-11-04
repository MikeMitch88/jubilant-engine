#!/usr/bin/env python3
"""
Diagnostic script to identify 404 issues
Run this to check your setup
"""

import subprocess
import requests
import sys
import time
from pathlib import Path

print("🔍 CODEBASE GENIUS - 404 DIAGNOSTIC TOOL")
print("=" * 60)

# Check 1: Project directory
print("\n[1/6] Checking project directory...")
project_dir = Path("/mnt/user-data/outputs/codebase-genius-fixed")
if project_dir.exists():
    print(f"✅ Project directory exists: {project_dir}")
else:
    print(f"❌ Project directory NOT found: {project_dir}")
    sys.exit(1)

# Check 2: Required files
print("\n[2/6] Checking required files...")
required_files = ["server.py", "app.py", "analyze_direct.py", "requirements.txt"]
missing_files = []
for file in required_files:
    file_path = project_dir / file
    if file_path.exists():
        print(f"✅ {file}")
    else:
        print(f"❌ {file} - MISSING!")
        missing_files.append(file)

if missing_files:
    print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
    print("Please ensure all project files are present.")
    sys.exit(1)

# Check 3: Check if server is running
print("\n[3/6] Checking if backend server is running...")
try:
    response = requests.get("http://localhost:8000/health", timeout=2)
    if response.status_code == 200:
        print(f"✅ Backend server is RUNNING on port 8000")
        print(f"   Response: {response.json()}")
    else:
        print(f"⚠️  Backend responding but with status {response.status_code}")
except requests.exceptions.ConnectionError:
    print("❌ Backend server is NOT running on port 8000")
    print("\n💡 To fix: Run in a terminal:")
    print(f"   cd {project_dir}")
    print("   python3 server.py")
except requests.exceptions.Timeout:
    print("⚠️  Backend server timed out")
except Exception as e:
    print(f"❌ Error connecting to backend: {e}")

# Check 4: Test all endpoints
print("\n[4/6] Testing API endpoints...")
endpoints = [
    ("GET", "/", "Root endpoint"),
    ("GET", "/health", "Health check"),
    ("GET", "/history", "History"),
]

for method, endpoint, description in endpoints:
    url = f"http://localhost:8000{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=2)
        elif method == "POST":
            response = requests.post(url, json={}, timeout=2)
        
        if response.status_code in [200, 201]:
            print(f"✅ {method} {endpoint} - {description}")
        elif response.status_code == 404:
            print(f"❌ {method} {endpoint} - 404 NOT FOUND")
        else:
            print(f"⚠️  {method} {endpoint} - Status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"❌ {method} {endpoint} - Cannot connect (server not running?)")
    except Exception as e:
        print(f"❌ {method} {endpoint} - Error: {str(e)[:50]}")

# Check 5: Check ports
print("\n[5/6] Checking port usage...")
try:
    # Check port 8000
    result_8000 = subprocess.run(
        ["lsof", "-i", ":8000"],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result_8000.stdout:
        print("✅ Port 8000 is in use:")
        for line in result_8000.stdout.split('\n')[1:3]:  # Show first 2 processes
            if line.strip():
                print(f"   {line}")
    else:
        print("❌ Port 8000 is NOT in use (backend not running)")
    
    # Check port 8501
    result_8501 = subprocess.run(
        ["lsof", "-i", ":8501"],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result_8501.stdout:
        print("✅ Port 8501 is in use (Streamlit likely running):")
        for line in result_8501.stdout.split('\n')[1:3]:
            if line.strip():
                print(f"   {line}")
    else:
        print("ℹ️  Port 8501 is NOT in use (Streamlit not running)")
        
except FileNotFoundError:
    print("ℹ️  'lsof' command not available, skipping port check")
except Exception as e:
    print(f"⚠️  Error checking ports: {e}")

# Check 6: Python packages
print("\n[6/6] Checking Python packages...")
required_packages = ["fastapi", "uvicorn", "streamlit", "requests"]
missing_packages = []

for package in required_packages:
    try:
        __import__(package)
        print(f"✅ {package}")
    except ImportError:
        print(f"❌ {package} - NOT INSTALLED")
        missing_packages.append(package)

if missing_packages:
    print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
    print("To install: pip install -r requirements.txt --break-system-packages")

# Summary and recommendations
print("\n" + "=" * 60)
print("📊 DIAGNOSTIC SUMMARY")
print("=" * 60)

issues_found = []
recommendations = []

# Analyze results
try:
    response = requests.get("http://localhost:8000/health", timeout=2)
    if response.status_code != 200:
        issues_found.append("Backend not responding correctly")
except:
    issues_found.append("Backend server not running")
    recommendations.append("Start backend: python3 server.py")

if missing_packages:
    issues_found.append(f"Missing packages: {', '.join(missing_packages)}")
    recommendations.append("Install: pip install -r requirements.txt --break-system-packages")

if not issues_found:
    print("\n✅ ALL CHECKS PASSED!")
    print("\nYour setup looks good. If you're still seeing 404 errors:")
    print("1. Check browser console (F12) for the exact failing URL")
    print("2. Check backend terminal for error messages")
    print("3. Verify Streamlit is connecting to http://localhost:8000")
else:
    print("\n⚠️  ISSUES FOUND:")
    for i, issue in enumerate(issues_found, 1):
        print(f"{i}. {issue}")
    
    print("\n💡 RECOMMENDATIONS:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")

print("\n" + "=" * 60)
print("📖 For detailed troubleshooting, see: TROUBLESHOOT_404.md")
print("=" * 60)
