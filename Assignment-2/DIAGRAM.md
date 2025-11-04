# System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE LAYER                         │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │              Streamlit Web Application                      │   │
│  │  • Repository URL Input                                     │   │
│  │  • Real-time Progress Display                               │   │
│  │  • Documentation Preview                                    │   │
│  │  • Download Functionality                                   │   │
│  │  • Analysis History Sidebar                                 │   │
│  └────────────────┬───────────────────────────────────────────┘   │
└───────────────────┼──────────────────────────────────────────────┘
                    │ HTTP REST API
                    │ (localhost:8501 → localhost:8000)
┌───────────────────▼──────────────────────────────────────────────┐
│                        API GATEWAY LAYER                          │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                 FastAPI Server                             │ │
│  │                                                            │ │
│  │  Endpoints:                                                │ │
│  │  • POST /analyze    → Trigger analysis                     │ │
│  │  • GET  /health     → System status                        │ │
│  │  • GET  /history    → List analyses                        │ │
│  │  • GET  /download/  → Get documentation                    │ │
│  │  • GET  /view/      → Preview content                      │ │
│  └────────────────┬───────────────────────────────────────────┘ │
└───────────────────┼──────────────────────────────────────────────┘
                    │ subprocess.run(['jac', 'run', ...])
                    │
┌───────────────────▼──────────────────────────────────────────────┐
│                     JAC ORCHESTRATION LAYER                       │
│                    (Multi-Agent System)                           │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    Code Genius                             │ │
│  │                 (Supervisor Walker)                        │ │
│  │  • Receives repo URL                                       │ │
│  │  • Creates Repository node                                 │ │
│  │  • Orchestrates subordinate agents                         │ │
│  │  • Aggregates results                                      │ │
│  │  • Updates history                                         │ │
│  └────────┬──────────────┬──────────────┬────────────────────┘ │
│           │              │              │                       │
│     spawns│        spawns│        spawns│                       │
│           │              │              │                       │
│  ┌────────▼────────┐ ┌──▼────────────┐ ┌▼─────────────────┐  │
│  │  Repo Mapper    │ │ Code Analyzer │ │    DocGenie      │  │
│  │   (Walker)      │ │   (Walker)    │ │    (Walker)      │  │
│  ├─────────────────┤ ├───────────────┤ ├──────────────────┤  │
│  │ • Clone repo    │ │ • Parse files │ │ • Collect data   │  │
│  │ • Map structure │ │ • Extract AST │ │ • Generate MD    │  │
│  │ • Read README   │ │ • Build CCG   │ │ • Create diagrams│  │
│  │ • Create        │ │ • Map relations│ │ • Save output   │  │
│  │   FileTree node │ │ • Create      │ │ • Create         │  │
│  │                 │ │   CodeGraph   │ │   Documentation  │  │
│  │                 │ │   node        │ │   node           │  │
│  └─────────────────┘ └───────────────┘ └──────────────────┘  │
│                                                                │
│  Graph Structure:                                              │
│  Repository → FileTree → CodeGraph → Documentation            │
│                                                                │
└───────────────────┬───────────────────────────────────────────┘
                    │ import py_module
                    │
┌───────────────────▼───────────────────────────────────────────┐
│                   PYTHON HELPER LAYER                          │
│                                                                │
│  ┌──────────────────┐ ┌─────────────────┐ ┌────────────────┐ │
│  │  repo_manager.py │ │ parse_code.py   │ │doc_generator.py│ │
│  ├──────────────────┤ ├─────────────────┤ ├────────────────┤ │
│  │• clone_repo()    │ │• generate_tree()│ │• generate_md() │ │
│  │• cleanup_repo()  │ │• parse_python() │ │• create_tree() │ │
│  │• read_readme()   │ │• parse_repo()   │ │• mermaid_graph│ │
│  └──────────────────┘ └─────────────────┘ └────────────────┘ │
│           │                    │                    │          │
└───────────┼────────────────────┼────────────────────┼──────────┘
            │                    │                    │
            │                    │                    │
┌───────────▼────────────────────▼────────────────────▼──────────┐
│                    EXTERNAL DEPENDENCIES                        │
│                                                                 │
│  ┌───────────┐  ┌───────────┐  ┌──────────┐  ┌──────────────┐│
│  │ GitPython │  │Python AST │  │ Markdown │  │ File System  ││
│  └───────────┘  └───────────┘  └──────────┘  └──────────────┘│
└─────────────────────────────────────────────────────────────────┘


DATA FLOW:
──────────

1. User enters GitHub URL in Streamlit UI
2. Streamlit sends POST request to FastAPI /analyze
3. FastAPI spawns JacLang AnalyzeRepo walker
4. Code Genius creates Repository node
5. Code Genius spawns Repo Mapper
   → Clones repo, creates FileTree node
6. Repo Mapper spawns Code Analyzer
   → Parses code, creates CodeGraph node
7. Code Analyzer spawns DocGenie
   → Generates documentation, creates Documentation node
8. Code Genius collects results
9. FastAPI returns response with output path
10. Streamlit displays results and download link


AGENT COMMUNICATION:
────────────────────

Agents communicate via:
• Graph node connections (++> operator)
• Walker spawning (spawn ... on ...)
• Shared node attributes (here.attribute)
• Python helper return values


FILE STRUCTURE:
───────────────

codebase-genius/
│
├── main.jac                    # Core JacLang agents
├── server.py                   # FastAPI REST API
├── app.py                      # Streamlit frontend
│
├── py_helpers/                 # Python utilities
│   ├── repo_manager.py        # Git operations
│   ├── parse_code.py          # AST parsing
│   └── doc_generator.py       # Markdown generation
│
├── outputs/                    # Generated documentation
│   └── <repo_name>/
│       └── documentation.md
│
├── requirements.txt            # Dependencies
├── README.md                   # Main documentation
├── ARCHITECTURE.md             # This diagram explained
├── QUICKSTART.md              # Quick setup guide
└── test_setup.py              # Setup verification


TECHNOLOGY STACK:
─────────────────

┌─────────────────────────────────────────────┐
│ Frontend:   Streamlit + Custom CSS         │
│ API:        FastAPI + Uvicorn              │
│ Core:       JacLang + Walker Pattern       │
│ Parsing:    Python AST                     │
│ VCS:        GitPython                      │
│ Diagrams:   Mermaid Syntax                 │
└─────────────────────────────────────────────┘
```

## Key Design Principles

1. **Agent Autonomy**: Each agent is responsible for its domain
2. **Graph-Based State**: Shared state via JacLang graph nodes
3. **Walker Orchestration**: Supervisor pattern with spawning
4. **Separation of Concerns**: API, Logic, and Helpers are distinct
5. **Fail-Safe**: Errors are captured and reported gracefully
6. **Scalable**: Pipeline architecture allows parallel processing
