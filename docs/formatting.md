# Code Formatting with Black

This project uses [Black](https://black.readthedocs.io/) for automatic Python code formatting.

## Configuration

Black is configured in `pyproject.toml` with the following settings:

- **Line length**: 120 characters
- **Target version**: Python 3.14
- **String normalization**: Enabled (converts single quotes to double quotes)
- **Magic trailing comma**: Enabled (respects trailing commas for formatting)

## Usage

### Format all files
```bash
black .
```

### Format specific directory
```bash
black src/
black tests/
```

### Check formatting without making changes
```bash
black --check .
```

### Show diff of what would be changed
```bash
black --check --diff .
```

## Integration

### Pre-commit Hook (Recommended)
You can set up a pre-commit hook to automatically format code before committing:

```bash
pip install pre-commit
```

Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 25.12.0
    hooks:
      - id: black
        language_version: python3.14
```

Then run:
```bash
pre-commit install
```

### IDE Integration

#### VS Code
Install the "Black Formatter" extension and add to `.vscode/settings.json`:
```json
{
  "python.formatting.provider": "black",
  "editor.formatOnSave": true
}
```

#### PyCharm
1. Go to Settings → Tools → Black
2. Enable "On code reformat" and "On save"

## Running Black

Black is installed as a development dependency. To install it:

```bash
pip install -e ".[dev]"
```

This will install black along with other development tools (pytest, hypothesis, isort, etc.).
