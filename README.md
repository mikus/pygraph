# PyGraph - Python Graph Library

A Python library providing efficient graph data structures and common graph algorithms.

## Features

- Graph data structures (directed/undirected, weighted/unweighted)
- Tree data structures with specialized algorithms
- Common graph algorithms (BFS, DFS, Dijkstra, MST, etc.)
- Property-based testing for correctness
- Modern Python 3.14+ with type hints

## Installation

```bash
# Install in development mode
pip install -e '.[dev]'
```

## Development

### Running Quality Checks

The project includes a unified quality check command that runs all checks:

```bash
check
```

This command runs:
1. **isort** - Import sorting check
2. **black** - Code formatting check
3. **prospector** - Comprehensive code quality analysis with integrated tools:
   - pylint, pyflakes, mccabe, pycodestyle (base tools)
   - ruff (fast linting)
   - pyright (type checking)
   - bandit (security analysis)
   - pyroma (package quality)
   - vulture (dead code detection)
4. **mypy** - Static type checking (run separately)
5. **pytest** - Tests with coverage report

### Individual Commands

You can also run individual tools:

```bash
# Format code
black src/ tests/
isort src/ tests/

# Check formatting without modifying
black --check src/ tests/
isort --check-only src/ tests/

# Run linting
ruff check src/ tests/                    # Fast linting

# Run comprehensive analysis with prospector (includes integrated tools)
prospector src/ tests/ --with-tool ruff --with-tool pyright --with-tool bandit --with-tool pyroma --with-tool vulture

# Run mypy separately (run separately due to prospector I/O issues)
mypy src/

# Run tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=src --cov-report=term-missing --cov-report=html
```

## Project Structure

```
pygraph/
├── src/              # Source code
├── tests/            # Test files
├── scripts/          # Development scripts
├── docs/             # Documentation
└── pyproject.toml    # Project configuration
```

## Requirements

- Python 3.14 or higher
- See `pyproject.toml` for full dependency list

## License

Apache 2.0 License
