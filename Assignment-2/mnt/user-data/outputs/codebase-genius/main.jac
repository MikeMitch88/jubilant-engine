"""
Codebase Genius - Agentic Code Documentation System
Main Jac implementation with multi-agent architecture
"""

import:py from datetime { datetime }
import:py from pathlib { Path }
import:py json;
import:py os;

# Import Python helper modules
import:py from py_helpers.parse_code { parse_repository, generate_tree_structure }
import:py from py_helpers.repo_manager { clone_repository, cleanup_repository }
import:py from py_helpers.doc_generator { generate_markdown_doc }

# Global state for tracking analyses
glob analysis_history: list = [];

# Node definitions
node Repository {
    has repo_url: str;
    has repo_name: str;
    has clone_path: str;
    has status: str = "pending";
    has error_msg: str = "";
    has created_at: str;
}

node FileTree {
    has structure: dict;
    has file_count: int;
    has summary: str = "";
}

node CodeGraph {
    has modules: dict;
    has classes: dict;
    has functions: dict;
    has relationships: list;
}

node Documentation {
    has content: str;
    has output_path: str;
    has generated_at: str;
}

# Walker: Code Genius (Supervisor)
walker CodeGenius {
    has repo_url: str;
    has workspace: str = "/tmp/codebase_genius";
    has results: dict = {};
    
    can initialize with Repository entry {
        # Set up workspace
        if not os.path.exists(self.workspace):
            os.makedirs(self.workspace);
        
        # Update repository node
        here.repo_url = self.repo_url;
        here.repo_name = self.repo_url.split('/')[-1].replace('.git', '');
        here.created_at = datetime.now().isoformat();
        here.status = "cloning";
        
        print(f"[CodeGenius] Starting analysis for: {here.repo_name}");
        
        # Spawn RepoMapper
        spawn RepoMapper(repo_url=self.repo_url, workspace=self.workspace) on here;
    }
    
    can process_results with Repository entry {
        # Collect all connected nodes
        file_tree_nodes = [n for n in here --> if n.__class__.__name__ == "FileTree"];
        code_graph_nodes = [n for n in here --> if n.__class__.__name__ == "CodeGraph"];
        doc_nodes = [n for n in here --> if n.__class__.__name__ == "Documentation"];
        
        if len(doc_nodes) > 0 {
            here.status = "completed";
            doc = doc_nodes[0];
            self.results = {
                "repo_name": here.repo_name,
                "status": "success",
                "output_path": doc.output_path,
                "generated_at": doc.generated_at
            };
            
            # Add to global history
            analysis_history.append(self.results);
            
            print(f"[CodeGenius] Analysis complete! Documentation saved to: {doc.output_path}");
        }
    }
}

# Walker: Repo Mapper
walker RepoMapper {
    has repo_url: str;
    has workspace: str;
    has clone_path: str = "";
    
    can map_repository with Repository entry {
        print(f"[RepoMapper] Cloning repository...");
        here.status = "mapping";
        
        # Clone the repository
        result = clone_repository(self.repo_url, self.workspace);
        
        if result["success"] {
            self.clone_path = result["clone_path"];
            here.clone_path = self.clone_path;
            
            print(f"[RepoMapper] Repository cloned to: {self.clone_path}");
            
            # Generate file tree structure
            tree_data = generate_tree_structure(self.clone_path);
            
            # Create FileTree node
            file_tree = FileTree(
                structure=tree_data["structure"],
                file_count=tree_data["file_count"],
                summary=tree_data["summary"]
            );
            here ++> file_tree;
            
            print(f"[RepoMapper] Mapped {tree_data['file_count']} files");
            
            # Spawn CodeAnalyzer
            spawn CodeAnalyzer(clone_path=self.clone_path) on here;
        } else {
            here.status = "failed";
            here.error_msg = result["error"];
            print(f"[RepoMapper] Error: {result['error']}");
        }
    }
}

# Walker: Code Analyzer
walker CodeAnalyzer {
    has clone_path: str;
    has analysis_data: dict = {};
    
    can analyze_code with Repository entry {
        print(f"[CodeAnalyzer] Analyzing code structure...");
        here.status = "analyzing";
        
        # Parse repository code
        analysis_result = parse_repository(self.clone_path);
        self.analysis_data = analysis_result;
        
        # Create CodeGraph node
        code_graph = CodeGraph(
            modules=analysis_result.get("modules", {}),
            classes=analysis_result.get("classes", {}),
            functions=analysis_result.get("functions", {}),
            relationships=analysis_result.get("relationships", [])
        );
        here ++> code_graph;
        
        print(f"[CodeAnalyzer] Found {len(analysis_result.get('modules', {}))} modules, "
              f"{len(analysis_result.get('classes', {}))} classes, "
              f"{len(analysis_result.get('functions', {}))} functions");
        
        # Spawn DocGenie
        spawn DocGenie(repo_name=here.repo_name, clone_path=self.clone_path) on here;
    }
}

# Walker: DocGenie
walker DocGenie {
    has repo_name: str;
    has clone_path: str;
    has output_dir: str = "outputs";
    
    can generate_documentation with Repository entry {
        print(f"[DocGenie] Generating documentation...");
        here.status = "documenting";
        
        # Get all connected data nodes
        file_tree_nodes = [n for n in here --> if n.__class__.__name__ == "FileTree"];
        code_graph_nodes = [n for n in here --> if n.__class__.__name__ == "CodeGraph"];
        
        file_tree = file_tree_nodes[0] if len(file_tree_nodes) > 0 else None;
        code_graph = code_graph_nodes[0] if len(code_graph_nodes) > 0 else None;
        
        # Generate markdown documentation
        doc_data = {
            "repo_name": self.repo_name,
            "clone_path": self.clone_path,
            "file_tree": file_tree.structure if file_tree else {},
            "file_count": file_tree.file_count if file_tree else 0,
            "summary": file_tree.summary if file_tree else "",
            "modules": code_graph.modules if code_graph else {},
            "classes": code_graph.classes if code_graph else {},
            "functions": code_graph.functions if code_graph else {},
            "relationships": code_graph.relationships if code_graph else []
        };
        
        result = generate_markdown_doc(doc_data, self.output_dir);
        
        if result["success"] {
            # Create Documentation node
            doc = Documentation(
                content=result["content"],
                output_path=result["output_path"],
                generated_at=datetime.now().isoformat()
            );
            here ++> doc;
            
            print(f"[DocGenie] Documentation generated: {result['output_path']}");
            
            # Cleanup cloned repository
            cleanup_repository(self.clone_path);
        } else {
            here.status = "failed";
            here.error_msg = result.get("error", "Documentation generation failed");
            print(f"[DocGenie] Error: {result.get('error')}");
        }
    }
}

# Walker for API endpoints
walker AnalyzeRepo {
    has repo_url: str;
    has result: dict = {};
    
    can start with `root entry {
        print(f"\n{'='*60}");
        print(f"Starting analysis for: {self.repo_url}");
        print(f"{'='*60}\n");
        
        # Create Repository node
        repo = Repository();
        root ++> repo;
        
        # Start CodeGenius walker
        genius = spawn CodeGenius(repo_url=self.repo_url) on repo;
        visit repo;
        
        # Process results
        genius_walker = spawn CodeGenius(repo_url=self.repo_url) on repo;
        genius_walker.process_results();
        self.result = genius_walker.results;
    }
}

walker GetHistory {
    has history: list = [];
    
    can get_all with `root entry {
        self.history = analysis_history;
    }
}

walker HealthCheck {
    has status: dict = {};
    
    can check with `root entry {
        self.status = {
            "status": "ok",
            "service": "Codebase Genius API",
            "timestamp": datetime.now().isoformat(),
            "analyses_count": len(analysis_history)
        };
    }
}
