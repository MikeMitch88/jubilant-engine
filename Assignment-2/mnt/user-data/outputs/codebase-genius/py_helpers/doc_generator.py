"""
Documentation Generator - Creates markdown documentation from analysis data
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List


def generate_tree_ascii(structure: dict, prefix: str = "", is_last: bool = True) -> str:
    """
    Generate ASCII tree representation of file structure.
    
    Args:
        structure: Nested dict representing file tree
        prefix: Current prefix for tree lines
        is_last: Whether this is the last item at current level
        
    Returns:
        ASCII tree string
    """
    lines = []
    items = list(structure.items())
    
    for i, (name, value) in enumerate(items):
        is_last_item = (i == len(items) - 1)
        
        # Current item connector
        connector = "└── " if is_last_item else "├── "
        lines.append(f"{prefix}{connector}{name}")
        
        # If directory, recurse
        if isinstance(value, dict) and value:
            # Extension for nested items
            extension = "    " if is_last_item else "│   "
            subtree = generate_tree_ascii(value, prefix + extension, is_last_item)
            lines.append(subtree)
    
    return "\n".join(lines)


def generate_mermaid_graph(relationships: List[Dict], max_nodes: int = 20) -> str:
    """
    Generate Mermaid diagram for code relationships.
    
    Args:
        relationships: List of relationship dicts
        max_nodes: Maximum number of nodes to include
        
    Returns:
        Mermaid diagram string
    """
    if not relationships:
        return "```mermaid\ngraph LR\n    A[No relationships found]\n```"
    
    # Filter to most important relationships
    filtered = []
    seen_pairs = set()
    
    for rel in relationships:
        if rel['type'] in ['inherits', 'imports']:
            from_node = rel.get('from', '').split('/')[-1].replace('.py', '').replace('.jac', '')
            to_node = rel.get('to', '').split('.')[-1]
            
            if from_node and to_node:
                pair = (from_node, to_node)
                if pair not in seen_pairs and len(filtered) < max_nodes:
                    filtered.append((from_node, to_node, rel['type']))
                    seen_pairs.add(pair)
    
    if not filtered:
        return "```mermaid\ngraph LR\n    A[No significant relationships]\n```"
    
    lines = ["```mermaid", "graph TD"]
    
    for from_node, to_node, rel_type in filtered:
        # Sanitize node names for Mermaid
        from_safe = from_node.replace('-', '_').replace(' ', '_')
        to_safe = to_node.replace('-', '_').replace(' ', '_')
        
        if rel_type == 'inherits':
            lines.append(f"    {from_safe}[{from_node}] -->|inherits| {to_safe}[{to_node}]")
        elif rel_type == 'imports':
            lines.append(f"    {from_safe}[{from_node}] -.->|imports| {to_safe}[{to_node}]")
    
    lines.append("```")
    return "\n".join(lines)


def generate_markdown_doc(doc_data: Dict, output_dir: str) -> Dict:
    """
    Generate comprehensive markdown documentation.
    
    Args:
        doc_data: Dictionary with all analysis data
        output_dir: Base output directory
        
    Returns:
        Dict with success status and output path
    """
    try:
        repo_name = doc_data.get('repo_name', 'unknown')
        
        # Create output directory
        repo_output_dir = os.path.join(output_dir, repo_name)
        os.makedirs(repo_output_dir, exist_ok=True)
        
        output_path = os.path.join(repo_output_dir, 'documentation.md')
        
        # Build markdown content
        md_lines = []
        
        # Header
        md_lines.extend([
            f"# {repo_name} - Code Documentation",
            "",
            f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
            "",
            "---",
            ""
        ])
        
        # Overview section
        md_lines.extend([
            "## 📖 Project Overview",
            ""
        ])
        
        summary = doc_data.get('summary', '')
        if summary:
            md_lines.extend([
                summary,
                ""
            ])
        else:
            md_lines.extend([
                "*No README summary available.*",
                ""
            ])
        
        # Statistics
        file_count = doc_data.get('file_count', 0)
        modules_count = len(doc_data.get('modules', {}))
        classes_count = len(doc_data.get('classes', {}))
        functions_count = len(doc_data.get('functions', {}))
        
        md_lines.extend([
            "### 📊 Repository Statistics",
            "",
            f"- **Total Files**: {file_count}",
            f"- **Python/Jac Modules**: {modules_count}",
            f"- **Classes**: {classes_count}",
            f"- **Functions**: {functions_count}",
            "",
            "---",
            ""
        ])
        
        # File Structure
        md_lines.extend([
            "## 📁 File Structure",
            "",
            "```",
            repo_name + "/"
        ])
        
        file_tree = doc_data.get('file_tree', {})
        if file_tree:
            tree_str = generate_tree_ascii(file_tree)
            md_lines.append(tree_str)
        
        md_lines.extend([
            "```",
            "",
            "---",
            ""
        ])
        
        # Modules and Classes
        md_lines.extend([
            "## 🏗️ Code Structure",
            ""
        ])
        
        modules = doc_data.get('modules', {})
        if modules:
            md_lines.extend([
                "### Modules",
                ""
            ])
            
            for module_path, module_data in sorted(modules.items())[:10]:  # Limit to 10
                md_lines.extend([
                    f"#### `{module_path}`",
                    ""
                ])
                
                if module_data.get('error'):
                    md_lines.extend([
                        f"*Parse error: {module_data['error']}*",
                        ""
                    ])
                    continue
                
                classes = module_data.get('classes', [])
                functions = module_data.get('functions', [])
                
                if classes:
                    md_lines.append("**Classes:**")
                    for cls in classes:
                        methods_str = ', '.join(cls['methods'][:5])
                        if len(cls['methods']) > 5:
                            methods_str += ', ...'
                        md_lines.append(f"- `{cls['name']}` - Methods: {methods_str or 'None'}")
                    md_lines.append("")
                
                if functions:
                    md_lines.append("**Functions:**")
                    for func in functions[:5]:  # Limit to 5
                        args_str = ', '.join(func['args'])
                        md_lines.append(f"- `{func['name']}({args_str})`")
                    if len(functions) > 5:
                        md_lines.append(f"- *... and {len(functions) - 5} more*")
                    md_lines.append("")
        
        md_lines.extend([
            "---",
            ""
        ])
        
        # Code Relationships
        md_lines.extend([
            "## 🔗 Code Relationships",
            ""
        ])
        
        relationships = doc_data.get('relationships', [])
        if relationships:
            # Generate Mermaid diagram
            mermaid = generate_mermaid_graph(relationships)
            md_lines.extend([
                mermaid,
                "",
                f"*Showing up to 20 key relationships from {len(relationships)} total.*",
                ""
            ])
        else:
            md_lines.extend([
                "*No relationships detected.*",
                ""
            ])
        
        md_lines.extend([
            "---",
            ""
        ])
        
        # API Reference
        md_lines.extend([
            "## 📚 API Reference",
            ""
        ])
        
        all_classes = doc_data.get('classes', {})
        if all_classes:
            md_lines.extend([
                "### Classes",
                "",
                "| Class | File | Methods |",
                "|-------|------|---------|"
            ])
            
            for class_name, class_data in sorted(all_classes.items())[:20]:  # Limit to 20
                simple_name = class_data['name']
                file_name = class_data['file']
                methods_count = len(class_data['methods'])
                md_lines.append(f"| `{simple_name}` | {file_name} | {methods_count} |")
            
            if len(all_classes) > 20:
                md_lines.append(f"| ... | ... | *{len(all_classes) - 20} more* |")
            
            md_lines.append("")
        
        all_functions = doc_data.get('functions', {})
        if all_functions:
            md_lines.extend([
                "### Functions",
                "",
                "| Function | File | Parameters |",
                "|----------|------|------------|"
            ])
            
            for func_name, func_data in sorted(all_functions.items())[:20]:  # Limit to 20
                simple_name = func_data['name']
                file_name = func_data['file']
                params = ', '.join(func_data['args'][:3])
                if len(func_data['args']) > 3:
                    params += ', ...'
                md_lines.append(f"| `{simple_name}` | {file_name} | {params or 'None'} |")
            
            if len(all_functions) > 20:
                md_lines.append(f"| ... | ... | *{len(all_functions) - 20} more* |")
            
            md_lines.append("")
        
        md_lines.extend([
            "---",
            "",
            "## 🎯 Summary",
            "",
            f"This documentation was automatically generated by **Codebase Genius**, "
            f"an agentic code documentation system. The analysis covered {modules_count} modules, "
            f"extracted {classes_count} classes and {functions_count} functions, and mapped "
            f"{len(relationships)} code relationships.",
            "",
            "*For more details, please refer to the source code or contact the repository maintainers.*"
        ])
        
        # Write to file
        content = "\n".join(md_lines)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "success": True,
            "output_path": output_path,
            "content": content
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Documentation generation failed: {str(e)}"
        }
