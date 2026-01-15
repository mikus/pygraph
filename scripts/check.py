#!/usr/bin/env python3
"""
Quality check script for the graph library project.
Runs tests, coverage, formatting checks, and linting.
"""

import subprocess
import sys
from pathlib import Path


def run_command(name: str, command: list[str], check: bool = True) -> bool:
    """Run a command and return success status."""
    print("=" * 60)
    print(f"Running: {name}")
    print("=" * 60)
    try:
        result = subprocess.run(command, check=check)
        if result.returncode == 0:
            print(f"✓ {name} passed\n")
            return True
        else:
            print(f"✗ {name} failed\n")
            return False
    except subprocess.CalledProcessError:
        print(f"✗ {name} failed\n")
        return False


def main():
    """Run all quality checks."""
    # Get project root directory
    project_root = Path(__file__).parent.parent
    
    print("\n" + "=" * 60)
    print("Running Quality Checks")
    print("=" * 60 + "\n")
    
    all_passed = True
    
    # 1. Check import sorting with isort
    if not run_command(
        "isort (import sorting check)",
        ["isort", "--check-only", "--diff", "src/", "tests/"],
        check=False
    ):
        all_passed = False
    
    # 2. Check code formatting with black
    if not run_command(
        "black (code formatting check)",
        ["black", "--check", "--diff", "src/", "tests/"],
        check=False
    ):
        all_passed = False
    
    # 3. Run pylint for code quality
    if not run_command(
        "pylint (code quality check)",
        ["pylint", "src/", "tests/", "--rcfile=pyproject.toml"],
        check=False
    ):
        all_passed = False
    
    # 4. Run tests with coverage
    if not run_command(
        "pytest (tests with coverage)",
        ["pytest", "tests/", "--cov=src", "--cov-report=term-missing", "--cov-report=html"],
        check=False
    ):
        all_passed = False
    
    # Final summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All checks passed!")
        print("=" * 60)
        return 0
    else:
        print("✗ Some checks failed!")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
