"""
CLI Wrapper for HealthCheck walker
Usage: jac run health_cli.jac
"""

import:jac from main {HealthCheck}

walker HealthCLI {
    can run with `root entry {
        checker = spawn HealthCheck() on root;
        print("Health check complete");
    }
}

# Entry point
with entry {
    health = spawn HealthCLI() on root;
}
