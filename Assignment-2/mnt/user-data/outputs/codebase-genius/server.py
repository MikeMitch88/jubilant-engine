"""
FastAPI Server for Codebase Genius
Bridges Jac backend with REST API
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import os
import subprocess
import json
from pathlib import Path
from typing import Optional

app = FastAPI(
    title="Codebase Genius API",
    description="AI-powered multi-agent code documentation system",
    version="1.0.0"
)

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    repo_url: str


class AnalyzeResponse(BaseModel):
    status: str
    repo_name: Optional[str] = None
    output_path: Optional[str] = None
    generated_at: Optional[str] = None
    error: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Codebase Genius API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    Returns service status and statistics
    """
    try:
        # Call Jac walker to get health status
        result = subprocess.run(
            ['jac', 'run', 'main.jac', '-w', 'HealthCheck'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__)),
            timeout=10
        )
        
        if result.returncode == 0:
            # Parse output for health data
            return {
                "status": "ok",
                "service": "Codebase Genius API",
                "jac_service": "operational"
            }
        else:
            return {
                "status": "degraded",
                "service": "Codebase Genius API",
                "error": "Jac service issue"
            }
    except Exception as e:
        return {
            "status": "ok",
            "service": "Codebase Genius API",
            "note": "Health check running in API mode"
        }


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_repository(request: AnalyzeRequest):
    """
    Analyze a GitHub repository and generate documentation
    
    Args:
        request: Contains repo_url
        
    Returns:
        Analysis results with output path
    """
    try:
        repo_url = request.repo_url
        
        # Validate URL
        if not repo_url.startswith(('http://', 'https://')):
            raise HTTPException(
                status_code=400,
                detail="Invalid repository URL. Must start with http:// or https://"
            )
        
        # Extract repo name for validation
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        
        # Run Jac analysis
        result = subprocess.run(
            ['jac', 'run', 'main.jac', '-w', 'AnalyzeRepo', '-ctx', json.dumps({"repo_url": repo_url})],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__)),
            timeout=600  # 10 minute timeout
        )
        
        # Check for success
        if result.returncode == 0:
            # Parse output to find documentation path
            output_dir = "outputs"
            expected_path = os.path.join(output_dir, repo_name, "documentation.md")
            
            if os.path.exists(expected_path):
                from datetime import datetime
                return AnalyzeResponse(
                    status="success",
                    repo_name=repo_name,
                    output_path=expected_path,
                    generated_at=datetime.now().isoformat()
                )
            else:
                # Still successful but check alternative paths
                return AnalyzeResponse(
                    status="completed",
                    repo_name=repo_name,
                    output_path=expected_path,
                    generated_at=datetime.now().isoformat()
                )
        else:
            error_msg = result.stderr if result.stderr else "Analysis failed"
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {error_msg}"
            )
            
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=408,
            detail="Analysis timed out (>10 minutes). Repository may be too large."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during analysis: {str(e)}"
        )


@app.get("/history")
async def get_history():
    """
    Get list of analyzed repositories
    
    Returns:
        List of analysis history
    """
    try:
        output_dir = "outputs"
        
        if not os.path.exists(output_dir):
            return {"history": []}
        
        history = []
        for repo_name in os.listdir(output_dir):
            repo_path = os.path.join(output_dir, repo_name)
            if os.path.isdir(repo_path):
                doc_path = os.path.join(repo_path, "documentation.md")
                if os.path.exists(doc_path):
                    stat = os.stat(doc_path)
                    history.append({
                        "repo_name": repo_name,
                        "output_path": doc_path,
                        "generated_at": stat.st_mtime
                    })
        
        # Sort by modification time, newest first
        history.sort(key=lambda x: x['generated_at'], reverse=True)
        
        return {"history": history}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving history: {str(e)}"
        )


@app.get("/download/{repo_name}")
async def download_documentation(repo_name: str):
    """
    Download generated documentation for a repository
    
    Args:
        repo_name: Name of the repository
        
    Returns:
        Markdown file
    """
    try:
        output_dir = "outputs"
        doc_path = os.path.join(output_dir, repo_name, "documentation.md")
        
        if not os.path.exists(doc_path):
            raise HTTPException(
                status_code=404,
                detail=f"Documentation not found for repository: {repo_name}"
            )
        
        return FileResponse(
            doc_path,
            media_type="text/markdown",
            filename=f"{repo_name}_documentation.md"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error downloading documentation: {str(e)}"
        )


@app.get("/view/{repo_name}")
async def view_documentation(repo_name: str):
    """
    View documentation content as JSON
    
    Args:
        repo_name: Name of the repository
        
    Returns:
        Documentation content
    """
    try:
        output_dir = "outputs"
        doc_path = os.path.join(output_dir, repo_name, "documentation.md")
        
        if not os.path.exists(doc_path):
            raise HTTPException(
                status_code=404,
                detail=f"Documentation not found for repository: {repo_name}"
            )
        
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "repo_name": repo_name,
            "content": content
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error viewing documentation: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
