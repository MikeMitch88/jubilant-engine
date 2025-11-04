#!/usr/bin/env python3
"""
Quick test script for Codebase Genius
Verifies basic functionality without full analysis
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import streamlit
        print("✅ Streamlit imported")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests imported")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        import git
        print("✅ GitPython imported")
    except ImportError as e:
        print(f"❌ GitPython import failed: {e}")
        return False
    
    return True


def test_helpers():
    """Test Python helper modules"""
    print("\n🔍 Testing helper modules...")
    
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from py_helpers import parse_code, repo_manager, doc_generator
        print("✅ Helper modules imported")
        return True
    except ImportError as e:
        print(f"❌ Helper import failed: {e}")
        return False


def test_directory_structure():
    """Test that required directories exist"""
    print("\n🔍 Testing directory structure...")
    
    required_dirs = ['py_helpers', 'outputs']
    required_files = ['main.jac', 'server.py', 'app.py', 'requirements.txt']
    
    all_good = True
    
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            print(f"✅ Directory '{dir_name}' exists")
        else:
            print(f"❌ Directory '{dir_name}' missing")
            all_good = False
    
    for file_name in required_files:
        if os.path.isfile(file_name):
            print(f"✅ File '{file_name}' exists")
        else:
            print(f"❌ File '{file_name}' missing")
            all_good = False
    
    return all_good


def test_git():
    """Test that git is available"""
    print("\n🔍 Testing Git availability...")
    
    import subprocess
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git available: {result.stdout.strip()}")
            return True
        else:
            print("❌ Git not available")
            return False
    except FileNotFoundError:
        print("❌ Git command not found")
        return False


def test_parser():
    """Test code parser with a simple example"""
    print("\n🔍 Testing code parser...")
    
    try:
        from py_helpers.parse_code import parse_python_file
        
        # Create a test file
        test_code = '''
def hello_world():
    """Test function"""
    return "Hello, World!"

class TestClass:
    def method(self):
        pass
'''
        
        with open('/tmp/test_parse.py', 'w') as f:
            f.write(test_code)
        
        result = parse_python_file('/tmp/test_parse.py')
        
        if result['functions'] and result['classes']:
            print(f"✅ Parser works: Found {len(result['functions'])} function(s) and {len(result['classes'])} class(es)")
            os.remove('/tmp/test_parse.py')
            return True
        else:
            print("❌ Parser didn't extract code elements")
            return False
            
    except Exception as e:
        print(f"❌ Parser test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("🧠 Codebase Genius - Setup Verification")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Helper Modules", test_helpers()))
    results.append(("Directory Structure", test_directory_structure()))
    results.append(("Git", test_git()))
    results.append(("Parser", test_parser()))
    
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:.<30} {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("=" * 60)
    if all_passed:
        print("🎉 All tests passed! System is ready.")
        print("\nNext steps:")
        print("1. Start the API server: uvicorn server:app --reload --port 8000")
        print("2. Start the UI: streamlit run app.py")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nTry running: pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
