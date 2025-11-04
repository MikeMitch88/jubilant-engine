"""
Code Parser - Analyzes Python and Jac code structure using AST
"""

import os
import ast
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict


def generate_tree_structure(repo_path: str) -> Dict:
    """
    Generate file tree structure for repository.
    
    Args:
        repo_path: Path to repository
        
    Returns:
        Dict with tree structure, file count, and summary
    """
    ignore_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 
                   'env', '.pytest_cache', '.mypy_cache', 'dist', 'build', '.idea'}
    ignore_files = {'.DS_Store', '.gitignore', '.gitattributes'}
    
    structure = {}
    file_count = 0
    file_types = defaultdict(int)
    
    def build_tree(path: str, parent: dict, depth: int = 0):
        nonlocal file_count
        
        if depth > 5:  # Limit depth to avoid deep nesting
            return
        
        try:
            items = sorted(os.listdir(path))
        except PermissionError:
            return
        
        for item in items:
            if item in ignore_files or item in ignore_dirs:
                continue
            
            item_path = os.path.join(path, item)
            
            if os.path.isdir(item_path):
                if item not in ignore_dirs:
                    parent[item] = {}
                    build_tree(item_path, parent[item], depth + 1)
            else:
                file_count += 1
                ext = Path(item).suffix
                file_types[ext] += 1
                parent[item] = "file"
    
    build_tree(repo_path, structure)
    
    # Read README
    from py_helpers.repo_manager import read_readme
    readme_content = read_readme(repo_path)
    summary = readme_content[:500] + "..." if len(readme_content) > 500 else readme_content
    
    return {
        "structure": structure,
        "file_count": file_count,
        "file_types": dict(file_types),
        "summary": summary
    }


def parse_python_file(file_path: str) -> Dict:
    """
    Parse a Python file using AST.
    
    Args:
        file_path: Path to Python file
        
    Returns:
        Dict with extracted code elements
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        tree = ast.parse(content)
        
        classes = []
        functions = []
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
                bases = [b.id if isinstance(b, ast.Name) else str(b) for b in node.bases]
                classes.append({
                    "name": node.name,
                    "methods": methods,
                    "bases": bases,
                    "lineno": node.lineno
                })
            
            elif isinstance(node, ast.FunctionDef):
                # Only top-level functions (not methods)
                if not any(isinstance(p, ast.ClassDef) for p in ast.walk(tree) 
                          if hasattr(p, 'body') and node in getattr(p, 'body', [])):
                    args = [arg.arg for arg in node.args.args]
                    functions.append({
                        "name": node.name,
                        "args": args,
                        "lineno": node.lineno
                    })
            
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "module": alias.name,
                        "alias": alias.asname
                    })
            
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append({
                        "module": f"{module}.{alias.name}" if module else alias.name,
                        "alias": alias.asname,
                        "from": module
                    })
        
        return {
            "classes": classes,
            "functions": functions,
            "imports": imports
        }
        
    except SyntaxError as e:
        return {
            "error": f"Syntax error: {str(e)}",
            "classes": [],
            "functions": [],
            "imports": []
        }
    except Exception as e:
        return {
            "error": f"Parse error: {str(e)}",
            "classes": [],
            "functions": [],
            "imports": []
        }


def parse_repository(repo_path: str) -> Dict:
    """
    Parse all Python and Jac files in repository.
    
    Args:
        repo_path: Path to repository
        
    Returns:
        Dict with complete code analysis
    """
    modules = {}
    all_classes = {}
    all_functions = {}
    relationships = []
    
    ignore_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 
                   'env', '.pytest_cache', '.mypy_cache', 'dist', 'build'}
    
    # Walk through repository
    for root, dirs, files in os.walk(repo_path):
        # Remove ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for file in files:
            if file.endswith('.py') or file.endswith('.jac'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, repo_path)
                
                # Parse file
                if file.endswith('.py'):
                    parsed = parse_python_file(file_path)
                else:
                    # Basic parsing for Jac files (treat similar to Python)
                    parsed = parse_python_file(file_path)
                
                modules[rel_path] = {
                    "classes": parsed.get("classes", []),
                    "functions": parsed.get("functions", []),
                    "imports": parsed.get("imports", []),
                    "error": parsed.get("error")
                }
                
                # Collect all classes and functions
                for cls in parsed.get("classes", []):
                    cls_full_name = f"{rel_path}::{cls['name']}"
                    all_classes[cls_full_name] = {
                        "file": rel_path,
                        "name": cls['name'],
                        "methods": cls['methods'],
                        "bases": cls['bases']
                    }
                    
                    # Add inheritance relationships
                    for base in cls['bases']:
                        relationships.append({
                            "type": "inherits",
                            "from": cls['name'],
                            "to": base,
                            "file": rel_path
                        })
                
                for func in parsed.get("functions", []):
                    func_full_name = f"{rel_path}::{func['name']}"
                    all_functions[func_full_name] = {
                        "file": rel_path,
                        "name": func['name'],
                        "args": func['args']
                    }
                
                # Add import relationships
                for imp in parsed.get("imports", []):
                    relationships.append({
                        "type": "imports",
                        "from": rel_path,
                        "to": imp['module']
                    })
    
    return {
        "modules": modules,
        "classes": all_classes,
        "functions": all_functions,
        "relationships": relationships
    }
