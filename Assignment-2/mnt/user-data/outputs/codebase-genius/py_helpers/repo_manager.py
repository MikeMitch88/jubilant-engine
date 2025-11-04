"""
Repository Manager - Handles cloning and cleanup of Git repositories
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict


def clone_repository(repo_url: str, workspace: str) -> Dict:
    """
    Clone a Git repository to the workspace.
    
    Args:
        repo_url: GitHub repository URL
        workspace: Base directory for cloning
        
    Returns:
        Dict with success status, clone_path, or error message
    """
    try:
        # Extract repo name
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        clone_path = os.path.join(workspace, repo_name)
        
        # Remove existing directory if present
        if os.path.exists(clone_path):
            shutil.rmtree(clone_path)
        
        # Clone repository
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', repo_url, clone_path],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            return {
                "success": True,
                "clone_path": clone_path,
                "repo_name": repo_name
            }
        else:
            return {
                "success": False,
                "error": f"Git clone failed: {result.stderr}"
            }
            
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Repository cloning timed out (>5 minutes)"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error cloning repository: {str(e)}"
        }


def cleanup_repository(clone_path: str) -> bool:
    """
    Clean up cloned repository directory.
    
    Args:
        clone_path: Path to cloned repository
        
    Returns:
        True if cleanup successful, False otherwise
    """
    try:
        if os.path.exists(clone_path):
            shutil.rmtree(clone_path)
            return True
        return True
    except Exception as e:
        print(f"Warning: Could not cleanup {clone_path}: {str(e)}")
        return False


def read_readme(repo_path: str) -> str:
    """
    Read README.md file from repository.
    
    Args:
        repo_path: Path to repository
        
    Returns:
        README content or empty string
    """
    readme_files = ['README.md', 'README.rst', 'README.txt', 'README']
    
    for readme_name in readme_files:
        readme_path = os.path.join(repo_path, readme_name)
        if os.path.exists(readme_path):
            try:
                with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
            except Exception as e:
                print(f"Error reading {readme_name}: {str(e)}")
                continue
    
    return ""
