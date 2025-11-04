"""
CLI Wrapper for running AnalyzeRepo walker
This file is executed with: jac run analyze_cli.jac <repo_url>
"""

import:py sys;
import:jac from main {AnalyzeRepo, Repository}

walker AnalyzeCLI {
    has repo_url: str = "";
    
    can run with `root entry {
        # Get repo URL from command line or stdin
        if len(sys.argv) > 1 {
            self.repo_url = sys.argv[1];
        }
        
        if not self.repo_url {
            print("Error: No repository URL provided");
            print("Usage: jac run analyze_cli.jac <repo_url>");
            return;
        }
        
        print(f"Analyzing repository: {self.repo_url}");
        
        # Create and run AnalyzeRepo walker
        analyzer = spawn AnalyzeRepo(repo_url=self.repo_url) on root;
        
        print("Analysis complete!");
    }
}

# Entry point
with entry {
    analyzer = spawn AnalyzeCLI() on root;
}
