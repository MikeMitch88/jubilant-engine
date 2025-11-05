"""
Streamlit Frontend for Codebase Genius
Dark theme UI with elegant design
"""

import streamlit as st
import requests
import time
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Codebase Genius",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme with gradient accents
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(90deg, #6C63FF 0%, #8E2DE2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(110, 99, 255, 0.3);
    }
    
    .header-title {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .header-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    /* Card styling */
    .card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Progress message styling */
    .progress-message {
        background: linear-gradient(90deg, rgba(108, 99, 255, 0.2) 0%, rgba(142, 45, 226, 0.2) 100%);
        border-left: 4px solid #6C63FF;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        color: white;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Success message */
    .success-box {
        background: linear-gradient(90deg, rgba(46, 213, 115, 0.2) 0%, rgba(0, 184, 148, 0.2) 100%);
        border-left: 4px solid #2ed573;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Error message */
    .error-box {
        background: linear-gradient(90deg, rgba(255, 71, 87, 0.2) 0%, rgba(255, 107, 107, 0.2) 100%);
        border-left: 4px solid #ff4757;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #6C63FF 0%, #8E2DE2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(108, 99, 255, 0.4);
    }
    
    /* Input styling */
    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        color: white;
        padding: 0.75rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(26, 26, 46, 0.95);
    }
    
    /* History item */
    .history-item {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 3px solid #6C63FF;
    }
    
    /* Stats container */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .stat-box {
        flex: 1;
        background: rgba(108, 99, 255, 0.1);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid rgba(108, 99, 255, 0.3);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #6C63FF;
    }
    
    .stat-label {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# API configuration
API_BASE_URL = os.getenv("API_URL", "https://codebase-genius-api.onrender.com")


def check_backend_health():
    """Check if backend is running (with cold start tolerance)"""
    try:
        # Longer timeout for Render free tier cold starts (can take 30-60 seconds)
        response = requests.get(f"{API_BASE_URL}/health", timeout=90)
        return response.status_code == 200
    except requests.exceptions.Timeout:
        return False
    except:
        return False


def analyze_repository(repo_url):
    """Send analysis request to backend"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json={"repo_url": repo_url},
            timeout=600  # 10 minute timeout
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "error": response.json().get("detail", "Unknown error")}
    except requests.exceptions.Timeout:
        return {"status": "error", "error": "Request timed out (>10 minutes)"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def get_history():
    """Get analysis history"""
    try:
        response = requests.get(f"{API_BASE_URL}/history", timeout=5)
        if response.status_code == 200:
            return response.json().get("history", [])
        return []
    except:
        return []


def view_documentation(repo_name):
    """Get documentation content"""
    try:
        response = requests.get(f"{API_BASE_URL}/view/{repo_name}", timeout=10)
        if response.status_code == 200:
            return response.json().get("content", "")
        return None
    except:
        return None


# Main app
def main():
    # Header
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🧠 Codebase Genius</h1>
        <p class="header-subtitle">AI-Powered Multi-Agent Code Documentation System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎛️ Control Panel")
        
        # Backend health check
        st.markdown("### System Status")

        with st.spinner("Checking backend status (may take 30-60s if waking up)..."):
            backend_healthy = check_backend_health()

        if backend_healthy:
            st.markdown("""
            <div class="success-box">
                ✅ Backend: <b>Online</b>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="error-box">
                ❌ Backend: <b>Offline</b><br>
                <small>Free tier may be sleeping. Try refreshing the page.</small>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # History
        st.markdown("### 📚 Recent Analyses")
        history = get_history()
        
        if history:
            for item in history[:5]:
                repo_name = item.get('repo_name', 'Unknown')
                with st.expander(f"📁 {repo_name}"):
                    if st.button(f"View {repo_name}", key=f"view_{repo_name}"):
                        st.session_state['view_repo'] = repo_name
        else:
            st.info("No analyses yet")
        
        st.markdown("---")
        
        # New Analysis button
        if st.button("➕ New Analysis", key="new_analysis"):
            st.session_state['view_repo'] = None
            st.rerun()
    
    # Main content
    if 'view_repo' in st.session_state and st.session_state['view_repo']:
        # View documentation mode
        repo_name = st.session_state['view_repo']
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"## 📄 Documentation: {repo_name}")
        with col2:
            if st.button("⬅️ Back to Analysis"):
                st.session_state['view_repo'] = None
                st.rerun()
        
        # Load and display documentation
        with st.spinner("Loading documentation..."):
            content = view_documentation(repo_name)
        
        if content:
            st.markdown(content)
            
            # Download button
            st.download_button(
                label="📥 Download Documentation",
                data=content,
                file_name=f"{repo_name}_documentation.md",
                mime="text/markdown"
            )
        else:
            st.error("Could not load documentation")
    
    else:
        # Analysis mode
        st.markdown("## 🚀 Analyze Repository")
        
        # Input form
        with st.form("analysis_form"):
            repo_url = st.text_input(
                "GitHub Repository URL",
                placeholder="https://github.com/username/repository",
                help="Enter the full URL of a public GitHub repository"
            )
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submit = st.form_submit_button("🔍 Analyze Repository")
        
        # Examples
        with st.expander("💡 Example Repositories"):
            st.markdown("""
            Try analyzing these example repositories:
            - `https://github.com/pallets/flask`
            - `https://github.com/psf/requests`
            - `https://github.com/django/django`
            - Any public Python or Jac repository
            """)
        
        # Process analysis
        if submit and repo_url:
            if not repo_url.startswith(('http://', 'https://')):
                st.error("❌ Please enter a valid URL starting with http:// or https://")
            else:
                # Progress container
                progress_container = st.container()
                
                with progress_container:
                    st.markdown("""
                    <div class="card">
                        <h3>🔄 Analysis in Progress</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Progress messages
                    messages = [
                        "🔍 Initializing Code Genius supervisor...",
                        "📥 Cloning repository...",
                        "🗺️ Mapping file structure...",
                        "🔬 Analyzing code with AST parser...",
                        "🧬 Building Code Context Graph...",
                        "📊 Extracting classes and functions...",
                        "🔗 Mapping relationships...",
                        "📝 Generating documentation...",
                        "✨ Finalizing output..."
                    ]
                    
                    progress_placeholder = st.empty()
                    
                    # Simulate progress display
                    for i, msg in enumerate(messages):
                        progress_placeholder.markdown(f"""
                        <div class="progress-message">
                            {msg}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if i == 1:  # Actually start analysis after showing first messages
                            # Call backend
                            result = analyze_repository(repo_url)
                        
                        time.sleep(0.5)
                    
                    progress_placeholder.empty()
                
                # Show results
                if result.get("status") in ["success", "completed"]:
                    st.markdown("""
                    <div class="success-box">
                        <h3>✅ Analysis Complete!</h3>
                        <p>Documentation has been generated successfully.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    repo_name = result.get("repo_name", "unknown")
                    output_path = result.get("output_path", "")
                    
                    # Show stats
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown("""
                        <div class="stat-box">
                            <div class="stat-value">✓</div>
                            <div class="stat-label">Status</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                        <div class="stat-box">
                            <div class="stat-value">📁</div>
                            <div class="stat-label">{repo_name}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col3:
                        st.markdown("""
                        <div class="stat-box">
                            <div class="stat-value">📄</div>
                            <div class="stat-label">Documentation</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # View and download buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("👁️ View Documentation", key="view_docs"):
                            st.session_state['view_repo'] = repo_name
                            st.rerun()
                    with col2:
                        if os.path.exists(output_path):
                            with open(output_path, 'r') as f:
                                content = f.read()
                            st.download_button(
                                label="📥 Download Markdown",
                                data=content,
                                file_name=f"{repo_name}_documentation.md",
                                mime="text/markdown"
                            )
                
                elif result.get("status") == "error":
                    st.markdown(f"""
                    <div class="error-box">
                        <h3>❌ Analysis Failed</h3>
                        <p>{result.get('error', 'Unknown error')}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Info section
        with st.expander("ℹ️ About Codebase Genius"):
            st.markdown("""
            **Codebase Genius** is an intelligent multi-agent system that automatically analyzes 
            code repositories and generates comprehensive documentation.
            
            **Features:**
            - 🤖 Multi-agent architecture (Code Genius, Repo Mapper, Code Analyzer, DocGenie)
            - 🗺️ Automatic repository structure mapping
            - 🔍 AST-based code analysis
            - 📊 Code Context Graph (CCG) generation
            - 🔗 Relationship and dependency mapping
            - 📝 Beautiful markdown documentation with diagrams
            - 🎨 Mermaid diagram generation
            
            **Supported Languages:** Python, JacLang
            """)


if __name__ == "__main__":
    main()
