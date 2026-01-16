#!/usr/bin/env python3
"""
Quality check script for the graph library project.
Runs tests, coverage, formatting checks, and comprehensive linting with prospector.
"""

import subprocess
import sys


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
        print(f"✗ {name} failed\n")
        return False
    except subprocess.CalledProcessError:
        print(f"✗ {name} failed\n")
        return False


def main():
    """Run all quality checks."""
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

    # 3. Run prospector for comprehensive code quality analysis
    # Includes base tools: pylint, pyflakes, mccabe, pycodestyle
    # Plus additional tools via --with-tool flags:
    #   - ruff (fast linting)
    #   - pyright (type checking)
    #   - bandit (security)
    #   - pyroma (package quality)
    #   - vulture (dead code detection)
    # Note: mypy is run separately below due to prospector I/O issues
    # Configuration is read from [tool.prospector] in pyproject.toml
    # Note: Scans project root, explicitly ignores scripts/ directory
    # Using python3 -m to ensure venv's prospector and tools are used
    if not run_command(
        "prospector (comprehensive code quality)",
        [
            sys.executable, "-m", "prospector",
            "--ignore-paths", "scripts",
            "--with-tool", "ruff",
            "--with-tool", "pyright",
            "--with-tool", "bandit",
            "--with-tool", "pyroma",
            "--with-tool", "vulture",
        ],
        check=False
    ):
        all_passed = False

    # 4. Run mypy separately (prospector has I/O issues with mypy)
    if not run_command(
        "mypy (static type checking)",
        [sys.executable, "-m", "mypy", "src/"],
        check=False
    ):
        all_passed = False

    # 5. Run tests with coverage
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
    print("✗ Some checks failed!")
    print("=" * 60)
    return 1


if __name__ == "__main__":
    sys.exit(main())
