#!/usr/bin/env python3
"""
Wrapper script to run Jac walkers with proper parameter passing
Usage: python run_walker.py <walker_name> <json_params>
"""

import sys
import json
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_walker.py <walker_name> [json_params]")
        sys.exit(1)
    
    walker_name = sys.argv[1]
    params = {}
    
    if len(sys.argv) >= 3:
        try:
            params = json.loads(sys.argv[2])
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON parameters: {e}")
            sys.exit(1)
    
    try:
        # Import the Jac module
        from jaclang import jac_import
        
        # Change to script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Import main.jac
        main_module = jac_import("main", base_path=script_dir)
        
        # Get the walker class
        walker_class = getattr(main_module, walker_name)
        
        # Create walker instance with parameters
        walker = walker_class(**params)
        
        # Execute the walker
        if hasattr(walker, 'start'):
            walker.start()
        elif hasattr(walker, 'check'):
            walker.check()
        elif hasattr(walker, 'get_all'):
            walker.get_all()
        
        # Output results if available
        if hasattr(walker, 'result'):
            print(json.dumps(walker.result, indent=2))
        elif hasattr(walker, 'status'):
            print(json.dumps(walker.status, indent=2))
        elif hasattr(walker, 'history'):
            print(json.dumps(walker.history, indent=2))
        
        sys.exit(0)
        
    except Exception as e:
        print(f"Error executing walker: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
