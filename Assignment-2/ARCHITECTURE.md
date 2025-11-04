# 🏗️ Codebase Genius - Architecture Documentation

## System Overview

Codebase Genius implements a **multi-agent architecture** inspired by the Jaseci Labs byLLM system. The system uses JacLang's walker-based programming paradigm to orchestrate intelligent agents that collaborate to analyze code repositories and generate documentation.

---

## 🤖 Agent Architecture

### 1. Code Genius (Supervisor Agent)

**Role**: Central orchestrator and workflow controller

**Responsibilities**:
- Receives GitHub repository URL from API
- Creates Repository node in the graph
- Spawns and coordinates subordinate agents
- Aggregates results from all agents
- Manages error handling and recovery
- Updates analysis history

**Walker Implementation**:
```jac
walker CodeGenius {
    has repo_url: str;
    has workspace: str;
    has results: dict;
    
    can initialize with Repository entry;
    can process_results with Repository entry;
}
```

**Workflow**:
1. Initialize workspace
2. Create Repository node
3. Spawn RepoMapper on Repository node
4. Wait for subordinate agents to complete
5. Collect and aggregate results
6. Update global history

---

### 2. Repo Mapper Agent

**Role**: Repository acquisition and structure mapping

**Responsibilities**:
- Clone Git repository using GitPython
- Generate file tree structure
- Extract README summary
- Filter irrelevant files/directories (.git, node_modules, etc.)
- Create FileTree node with metadata
- Spawn Code Analyzer for next stage

**Walker Implementation**:
```jac
walker RepoMapper {
    has repo_url: str;
    has workspace: str;
    has clone_path: str;
    
    can map_repository with Repository entry;
}
```

**Output**:
- FileTree node containing:
  - Nested directory structure
  - File count statistics
  - README summary
  - File type distribution

---

### 3. Code Analyzer Agent

**Role**: Source code parsing and analysis

**Responsibilities**:
- Walk through all Python and Jac files
- Parse code using Python AST
- Extract code elements:
  - Classes and methods
  - Functions and parameters
  - Import statements
  - Inheritance relationships
- Build Code Context Graph (CCG)
- Identify relationships and dependencies
- Create CodeGraph node
- Spawn DocGenie for documentation generation

**Walker Implementation**:
```jac
walker CodeAnalyzer {
    has clone_path: str;
    has analysis_data: dict;
    
    can analyze_code with Repository entry;
}
```

**Parsing Strategy**:
1. Use AST for Python files
2. Support Jac files (similar syntax)
3. Extract class hierarchies
4. Map function calls
5. Track import dependencies

---

### 4. DocGenie Agent

**Role**: Documentation generation and formatting

**Responsibilities**:
- Collect data from FileTree and CodeGraph nodes
- Generate markdown documentation with:
  - Project overview
  - File structure visualization (ASCII tree)
  - Code structure breakdown
  - Relationship diagrams (Mermaid)
  - API reference tables
- Save documentation to outputs directory
- Create Documentation node
- Clean up temporary files

**Walker Implementation**:
```jac
walker DocGenie {
    has repo_name: str;
    has clone_path: str;
    has output_dir: str;
    
    can generate_documentation with Repository entry;
}
```

**Documentation Sections**:
1. Header with metadata
2. Project overview and statistics
3. File structure tree
4. Code structure (modules, classes, functions)
5. Code relationships diagram
6. API reference tables
7. Summary

---

## 🔄 Data Flow

```
User Input (GitHub URL)
    ↓
FastAPI Server (/analyze endpoint)
    ↓
JacLang Runtime (AnalyzeRepo walker)
    ↓
Code Genius (Supervisor)
    ↓
Repo Mapper → FileTree Node
    ↓
Code Analyzer → CodeGraph Node
    ↓
DocGenie → Documentation Node
    ↓
FastAPI Response
    ↓
Streamlit UI Display
```

---

## 📊 Graph Structure

### Node Types

**Repository Node**:
```python
node Repository {
    has repo_url: str;
    has repo_name: str;
    has clone_path: str;
    has status: str;
    has error_msg: str;
    has created_at: str;
}
```

**FileTree Node**:
```python
node FileTree {
    has structure: dict;
    has file_count: int;
    has summary: str;
}
```

**CodeGraph Node**:
```python
node CodeGraph {
    has modules: dict;
    has classes: dict;
    has functions: dict;
    has relationships: list;
}
```

**Documentation Node**:
```python
node Documentation {
    has content: str;
    has output_path: str;
    has generated_at: str;
}
```

### Node Relationships

```
Repository Node
    └──> FileTree Node (connected via ++>)
            └──> CodeGraph Node
                    └──> Documentation Node
```

---

## 🔌 API Layer

### FastAPI Server (server.py)

**Purpose**: Bridge between HTTP requests and Jac backend

**Endpoints**:
- `POST /analyze`: Triggers Code Genius walker
- `GET /health`: System health check
- `GET /history`: Lists analyzed repositories
- `GET /download/{repo_name}`: Downloads documentation
- `GET /view/{repo_name}`: Returns documentation as JSON

**Integration Method**:
```python
subprocess.run([
    'jac', 'run', 'main.jac',
    '-w', 'AnalyzeRepo',
    '-ctx', json.dumps({"repo_url": repo_url})
])
```

---

## 🎨 Frontend Layer

### Streamlit UI (app.py)

**Features**:
- Repository URL input
- Real-time progress tracking
- Documentation preview
- Download functionality
- Analysis history sidebar
- Health monitoring

**Design Elements**:
- Dark theme with gradient accents (#6C63FF → #8E2DE2)
- Animated progress messages
- Responsive cards and containers
- Custom CSS styling

---

## 🧩 Python Helpers

### Module: py_helpers/repo_manager.py

**Functions**:
- `clone_repository(repo_url, workspace)`: Git clone with timeout
- `cleanup_repository(clone_path)`: Remove temporary files
- `read_readme(repo_path)`: Extract README content

### Module: py_helpers/parse_code.py

**Functions**:
- `generate_tree_structure(repo_path)`: Build file tree
- `parse_python_file(file_path)`: AST-based parsing
- `parse_repository(repo_path)`: Full repo analysis

### Module: py_helpers/doc_generator.py

**Functions**:
- `generate_tree_ascii(structure)`: ASCII tree visualization
- `generate_mermaid_graph(relationships)`: Mermaid diagrams
- `generate_markdown_doc(doc_data)`: Complete documentation

---

## 🔒 Security Considerations

1. **Repository Cloning**:
   - Only public repositories
   - Shallow clone (--depth 1) to save bandwidth
   - Timeout protection (5 minutes)

2. **File System**:
   - Temporary workspace isolation
   - Automatic cleanup after analysis
   - No persistent storage of cloned repos

3. **API**:
   - Input validation
   - Timeout limits
   - Error handling

---

## ⚡ Performance Optimizations

1. **Shallow Cloning**: Only fetch latest commit
2. **Selective Parsing**: Skip irrelevant directories
3. **Limited Depth**: File tree limited to 5 levels
4. **Result Caching**: Keep analysis history
5. **Concurrent Processing**: Agents work in pipeline

---

## 🔄 Error Handling

### Repository Level
- Clone failures → return error to user
- Invalid URLs → HTTP 400 response
- Timeout → HTTP 408 response

### Agent Level
- Parse errors → captured in module data
- Missing files → graceful skip
- Failed spawns → logged, workflow continues

### System Level
- API connection errors → shown in UI
- Backend offline → health check warning
- Disk space issues → early detection

---

## 🚀 Scalability

### Current Limitations
- Single repository at a time
- No parallel analysis
- In-memory history storage

### Future Enhancements
- Queue-based processing
- Database storage
- Redis caching
- Worker pool for parallel analysis
- Support for private repositories (with auth)

---

## 📈 Monitoring & Logging

### Jac Walker Logs
- Print statements for each agent action
- Progress tracking throughout pipeline
- Error messages with context

### API Logs
- Request/response logging
- Error stack traces
- Performance metrics

### UI Feedback
- Real-time progress messages
- Success/failure notifications
- Download statistics

---

## 🧪 Testing Strategy

1. **Unit Tests**: Individual helper functions
2. **Integration Tests**: Walker workflows
3. **End-to-End Tests**: Full API → UI flow
4. **Example Repositories**: Known good test cases

---

This architecture demonstrates the power of **agent-oriented programming** with JacLang, where autonomous agents collaborate through a shared graph structure to accomplish complex tasks efficiently.
