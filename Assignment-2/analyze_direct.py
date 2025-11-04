#!/usr/bin/env python3
"""
Direct Python implementation of the analysis workflow
This bypasses the Jac walker complexity for now
"""

import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from py_helpers.repo_manager import clone_repository, cleanup_repository
from py_helpers.parse_code import parse_repository, generate_tree_structure
from py_helpers.doc_generator import generate_markdown_doc


def analyze_repository(repo_url):
    """
    Analyze a repository and generate documentation
    """
    print(f"\n{'='*60}")
    print(f"Starting analysis for: {repo_url}")
    print(f"{'='*60}\n")
    
    # Step 1: Clone repository
    print("[1/4] Cloning repository...")
    workspace = "/tmp/codebase_genius"
    Path(workspace).mkdir(parents=True, exist_ok=True)
    
    clone_result = clone_repository(repo_url, workspace)
    
    if not clone_result["success"]:
        print(f"Error cloning repository: {clone_result['error']}")
        return {
            "success": False,
            "error": clone_result["error"]
        }
    
    clone_path = clone_result["clone_path"]
    repo_name = Path(clone_path).name
    
    print(f"Repository cloned to: {clone_path}")
    
    # Step 2: Generate file tree
    print("\n[2/4] Mapping file structure...")
    tree_data = generate_tree_structure(clone_path)
    print(f"Mapped {tree_data['file_count']} files")
    
    # Step 3: Parse code and build graph
    print("\n[3/4] Analyzing code structure...")
    analysis_result = parse_repository(clone_path)
    
    print(f"Found {len(analysis_result.get('modules', {}))} modules, "
          f"{len(analysis_result.get('classes', {}))} classes, "
          f"{len(analysis_result.get('functions', {}))} functions")
    
    # Step 4: Generate documentation
    print("\n[4/4] Generating documentation...")
    doc_data = {
        "repo_name": repo_name,
        "clone_path": clone_path,
        "file_tree": tree_data["structure"],
        "file_count": tree_data["file_count"],
        "summary": tree_data["summary"],
        "modules": analysis_result.get("modules", {}),
        "classes": analysis_result.get("classes", {}),
        "functions": analysis_result.get("functions", {}),
        "relationships": analysis_result.get("relationships", [])
    }
    
    output_dir = "outputs"
    doc_result = generate_markdown_doc(doc_data, output_dir)
    
    if doc_result["success"]:
        print(f"\nDocumentation generated: {doc_result['output_path']}")
        
        # Cleanup
        cleanup_repository(clone_path)
        
        return {
            "success": True,
            "repo_name": repo_name,
            "output_path": doc_result["output_path"],
            "content": doc_result["content"]
        }
    else:
        print(f"\nError generating documentation: {doc_result.get('error')}")
        cleanup_repository(clone_path)
        return {
            "success": False,
            "error": doc_result.get("error", "Documentation generation failed")
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_direct.py <repo_url>")
        sys.exit(1)
    
    repo_url = sys.argv[1]
    
    result = analyze_repository(repo_url)
    
    # Print JSON result
    print("\n" + "="*60)
    print("RESULT:")
    print(json.dumps(result, indent=2))
    print("="*60)
    
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
