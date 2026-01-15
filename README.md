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
3. **pylint** - Code quality and linting
4. **pytest** - Tests with coverage report

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
pylint src/ tests/ --rcfile=pyproject.toml

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
