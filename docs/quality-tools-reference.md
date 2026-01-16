# Quality Tools Quick Reference

## Overview

PyGraph uses a comprehensive suite of code quality tools to ensure high standards.

## Quick Commands

```bash
# Run everything (recommended before commit)
check

# Fast feedback loop during development
ruff check src/ tests/
black --check src/ tests/
isort --check-only src/ tests/

# Comprehensive analysis before PR
prospector src/ tests/ --with-tool ruff --with-tool pyright --with-tool bandit --with-tool pyroma --with-tool vulture
mypy src/
bandit -r src/
```

## Tool Breakdown

### 1. Black - Code Formatting
**Purpose**: Automatic code formatting  
**Speed**: ⚡⚡⚡ Very Fast  
**When**: Every save (IDE integration) or before commit

```bash
# Format code
black src/ tests/

# Check only (no changes)
black --check src/ tests/

# Show what would change
black --diff src/ tests/
```

**Configuration**: `[tool.black]` in `pyproject.toml`

---

### 2. isort - Import Sorting
**Purpose**: Organize imports consistently  
**Speed**: ⚡⚡⚡ Very Fast  
**When**: Every save (IDE integration) or before commit

```bash
# Sort imports
isort src/ tests/

# Check only (no changes)
isort --check-only src/ tests/

# Show what would change
isort --diff src/ tests/
```

**Configuration**: `[tool.isort]` in `pyproject.toml`

---

### 3. Ruff - Fast Linting
**Purpose**: Fast linting and error detection  
**Speed**: ⚡⚡⚡ Extremely Fast (Rust-based)  
**When**: Integrated with prospector (runs with all other tools)

```bash
# Via prospector (RECOMMENDED)
prospector src/ tests/ --with-tool ruff

# Standalone (if needed for quick feedback during development)
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/

# Show all violations
ruff check --show-files src/ tests/
```

**What it checks**:
- Syntax errors (pyflakes)
- Style issues (pycodestyle)
- Import order (isort rules)
- Naming conventions (pep8-naming)
- Code modernization (pyupgrade)
- Bug patterns (flake8-bugbear)
- Simplifications (flake8-simplify)

**Configuration**: `[tool.ruff]` in `pyproject.toml`

---

### 4. Prospector - Comprehensive Analysis
**Purpose**: Multi-tool code quality suite  
**Speed**: ⚡⚡ Moderate (runs 8+ tools)  
**When**: Before commit or PR

```bash
# Run all checks
prospector src/ tests/

# With all additional tools integrated (RECOMMENDED)
prospector src/ tests/ --with-tool ruff --with-tool pyright --with-tool bandit --with-tool pyroma --with-tool vulture

# Note: mypy is run separately, not via prospector
mypy src/

# With specific profile (optional - prospector reads from pyproject.toml by default)
prospector src/ tests/ --with-tool ruff --with-tool pyright

# JSON output for CI
prospector src/ tests/ --with-tool ruff --with-tool pyright --with-tool bandit --with-tool pyroma --with-tool vulture --output-format json
```

**Included tools**:
1. **pylint** - Code quality and style
2. **pyflakes** - Error detection
3. **mccabe** - Complexity analysis
4. **pycodestyle** - PEP 8 compliance
5. **ruff** - Fast linting (via --with-tool)
6. **pyright** - Type checking (via --with-tool)
7. **bandit** - Security scanning (via --with-tool)
8. **pyroma** - Package quality (via --with-tool)
9. **vulture** - Dead code detection (via --with-tool)

**Note**: mypy is run separately (not via prospector) due to I/O issues when integrated.

**Configuration**: `[tool.prospector]` in `pyproject.toml`

---

### 5. mypy - Type Checking
**Purpose**: Static type analysis  
**Speed**: ⚡⚡ Moderate  
**When**: Before commit or PR (run separately from prospector)

```bash
# Standalone (RECOMMENDED - run separately due to prospector I/O issues)
mypy src/

# Check specific file
mypy src/pygraph/graph.py

# Verbose output
mypy src/ --verbose
```

**Note**: mypy is run separately from prospector due to I/O errors when integrated. The `check` script runs it as a separate step.

**What it checks**:
- Type hint correctness
- Type compatibility
- Missing return types
- Unused type ignores
- Redundant casts

**Configuration**: `[tool.mypy]` in `pyproject.toml`

---

### 6. Pyright - Additional Type Checking
**Purpose**: Microsoft's type checker (catches different issues than mypy)  
**Speed**: ⚡⚡ Moderate  
**When**: Before commit or PR (integrated with prospector)

```bash
# Via prospector (RECOMMENDED)
prospector src/ tests/ --with-tool pyright

# Standalone (if needed)
pyright src/

# Check specific file
pyright src/pygraph/graph.py

# Verbose output
pyright src/ --verbose
```

**What it checks**:
- Type completeness
- Unused imports/variables
- Unreachable code
- Type narrowing issues

**Configuration**: `[tool.pyright]` in `pyproject.toml`

---

### 7. Bandit - Security Analysis
**Purpose**: Security vulnerability scanning  
**Speed**: ⚡⚡ Fast  
**When**: Before commit or PR (integrated with prospector)

```bash
# Via prospector (RECOMMENDED)
prospector src/ tests/ --with-tool bandit

# Standalone (if needed)
bandit -r src/

# With config
bandit -r src/ -c pyproject.toml

# JSON report
bandit -r src/ -f json -o bandit-report.json

# Specific severity
bandit -r src/ -ll  # Only medium and high severity
```

**What it checks**:
- SQL injection risks
- Shell injection risks
- Hardcoded passwords
- Insecure random usage
- Unsafe YAML loading
- And 40+ other security issues

**Configuration**: `[tool.bandit]` in `pyproject.toml`

---

### 8. Vulture - Dead Code Detection
**Purpose**: Find unused code  
**Speed**: ⚡⚡ Fast  
**When**: Periodically or before major refactoring (integrated with prospector)

```bash
# Via prospector (RECOMMENDED)
prospector src/ tests/ --with-tool vulture

# Standalone (if installed separately)
vulture src/
```

**What it finds**:
- Unused functions
- Unused classes
- Unused variables
- Unused imports
- Unreachable code

**Note**: May have false positives (e.g., protocol methods, test fixtures)

**Configuration**: `[tool.prospector.vulture]` in `pyproject.toml`

---

### 9. Pyroma - Package Quality
**Purpose**: Check package metadata and structure  
**Speed**: ⚡⚡⚡ Very Fast  
**When**: Before release or when updating package metadata (integrated with prospector)

```bash
# Via prospector (RECOMMENDED)
prospector src/ tests/ --with-tool pyroma

# Standalone (if installed separately)
pyroma .
```

**What it checks**:
- Package metadata completeness
- README quality
- License information
- Classifiers
- Long description
- Version format

**Configuration**: `[tool.prospector.pyroma]` in `pyproject.toml`

---

### 10. pytest - Testing
**Purpose**: Run tests with coverage  
**Speed**: ⚡ Depends on test suite  
**When**: Always (TDD workflow)

```bash
# Run all tests with coverage
pytest tests/

# Specific test file
pytest tests/test_graph_unit.py

# Specific test
pytest tests/test_graph_unit.py::test_graph_creation

# With coverage report
pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# Only unit tests
pytest -m unit tests/

# Only property tests
pytest -m property tests/
```

**Configuration**: `[tool.pytest.ini_options]` in `pyproject.toml`

---

## Recommended Workflow

### During Development (Fast Feedback)
```bash
# After making changes
ruff check src/ tests/              # < 1 second
black --check src/ tests/           # < 1 second
isort --check-only src/ tests/      # < 1 second
pytest tests/test_specific.py       # Seconds to minutes
```

### Before Commit (Comprehensive)
```bash
# Run everything (RECOMMENDED)
check

# Or manually:
black src/ tests/
isort src/ tests/
ruff check src/ tests/
prospector src/ tests/ --with-tool ruff --with-tool pyright --with-tool bandit --with-tool pyroma --with-tool vulture
mypy src/
pytest tests/ --cov=src
```

### Before PR (Extra Thorough)
```bash
# Run check command
check

# Review reports
open htmlcov/index.html              # Coverage report
prospector src/ tests/ --with-tool ruff --with-tool pyright --with-tool bandit --with-tool pyroma --with-tool vulture --output-format json > prospector-report.json
```

---

## IDE Integration

### VS Code
```json
{
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.linting.mypyEnabled": true,
  "python.linting.banditEnabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

### PyCharm
- Settings → Tools → Black → Enable
- Settings → Tools → External Tools → Add ruff, prospector
- Settings → Editor → Inspections → Enable mypy plugin

---

## Troubleshooting

### Ruff and Black Conflict
Ruff is configured to be compatible with Black. If conflicts occur, Black takes precedence.

### Type Checking Errors
Both mypy and pyright may report different issues. Fix both or configure exclusions.

### Bandit False Positives
Add `# nosec` comment or configure exclusions in `pyproject.toml`.

### Vulture False Positives
Adjust `min-confidence` in `[tool.prospector.vulture]` section of `pyproject.toml` or add exclusions.

### Prospector Takes Too Long
Run individual tools during development, prospector before commit.

---

## Performance Tips

1. **Use ruff for quick checks** during development
2. **Run prospector less frequently** (before commit/PR)
3. **Cache type checking results** (mypy/pyright have caching)
4. **Run tests in parallel** with `pytest -n auto` (requires pytest-xdist)
5. **Use IDE integration** for real-time feedback

---

## Quality Metrics

### Current Standards
- ✅ 100% test coverage (line and branch)
- ✅ All prospector checks pass
- ✅ No type errors (mypy and pyright)
- ✅ No security issues (bandit)
- ✅ No unused code (vulture)
- ✅ Black formatted
- ✅ isort organized

### Acceptable Exceptions
- Vulture false positives (protocol methods, test fixtures)
- Bandit false positives (with justification)
- Type ignore comments (with explanation)

---

## Further Reading

- **Black**: https://black.readthedocs.io/
- **isort**: https://pycqa.github.io/isort/
- **Ruff**: https://docs.astral.sh/ruff/
- **Prospector**: https://prospector.landscape.io/
- **mypy**: https://mypy.readthedocs.io/
- **Pyright**: https://github.com/microsoft/pyright
- **Bandit**: https://bandit.readthedocs.io/
- **Vulture**: https://github.com/jendrikseipp/vulture
- **Pyroma**: https://github.com/regebro/pyroma
