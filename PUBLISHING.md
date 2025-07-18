# Publishing to PyPI

This guide explains how to publish the ollama-utils package to PyPI using modern Python tooling with `uv`.

## Prerequisites

1. **PyPI Account**: Create accounts on [PyPI](https://pypi.org) and [TestPyPI](https://test.pypi.org)

2. **API Tokens**: Generate API tokens for both PyPI and TestPyPI:
   - PyPI: Account settings → API tokens → Add API token
   - TestPyPI: Account settings → API tokens → Add API token

3. **Install uv**: 
   ```bash
   # Install uv (modern Python package manager)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # or
   pip install uv
   ```

## Build Process

### 1. Update Version

Update the version in `pyproject.toml`:
```toml
[project]
name = "ollama-utils"
version = "0.1.1"  # Increment version
```

### 2. Set Up Development Environment

```bash
# Sync dependencies (including dev dependencies)
uv sync --dev
```

### 3. Build Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build the package using uv
uv build
```

This creates:
- `dist/ollama_utils-0.1.1.tar.gz` (source distribution)
- `dist/ollama_utils-0.1.1-py3-none-any.whl` (wheel distribution)

### 4. Test on TestPyPI

First, test the upload on TestPyPI:

```bash
# Upload to TestPyPI using uvx (uv's tool runner)
uvx twine upload --repository testpypi dist/*
```

When prompted, use:
- Username: `__token__`
- Password: Your TestPyPI API token

### 5. Test Installation

Test installing from TestPyPI:

```bash
# Create a temporary environment and test
uv venv test-env
source test-env/bin/activate  # On Windows: test-env\Scripts\activate

# Install from TestPyPI
uv pip install --index-url https://test.pypi.org/simple/ ollama-utils

# Test the package
python -c "import ollama_utils; print(ollama_utils.__version__)"

# Cleanup
deactivate
rm -rf test-env
```

### 6. Upload to PyPI

If TestPyPI works correctly, upload to PyPI:

```bash
# Upload to PyPI using uvx
uvx twine upload dist/*
```

When prompted, use:
- Username: `__token__`
- Password: Your PyPI API token

## Automated Publishing

### Using GitHub Actions

The repository includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:

1. **Runs tests** on every push and PR
2. **Builds package** on pushes to main
3. **Publishes to PyPI** on version tags

To use automated publishing:

1. Add your PyPI API token to GitHub Secrets:
   - Go to repository Settings → Secrets → Actions
   - Add `PYPI_API_TOKEN` with your PyPI token

2. Create a version tag:
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```

3. The workflow will automatically build and publish to PyPI

## Version Management

### Semantic Versioning

Follow [semantic versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH` (e.g., `1.0.0`)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Pre-release Versions

For pre-release versions:
- `1.0.0a1` (alpha)
- `1.0.0b1` (beta)
- `1.0.0rc1` (release candidate)

## Quality Checks

Before publishing, ensure:

1. **Tests pass**:
   ```bash
   uv run pytest tests/
   ```

2. **Code quality**:
   ```bash
   uv run flake8 ollama_utils/
   ```

3. **Type checking**:
   ```bash
   uv run mypy ollama_utils/
   ```

4. **Documentation is up to date**:
   - README.md
   - CHANGELOG.md (if applicable)
   - docstrings

5. **Package builds correctly**:
   ```bash
   uv build
   ```

## Package Structure Verification

Before publishing, verify the package structure:

```bash
# Check what will be included
uv build
tar -tzf dist/ollama_utils-*.tar.gz
```

Ensure all necessary files are included:
- Source code
- README.md
- LICENSE
- Examples
- Tests (optional)

## Troubleshooting

### Common Issues

1. **Version already exists**: 
   - PyPI doesn't allow re-uploading the same version
   - Increment version number

2. **Missing files**:
   - Check MANIFEST.in
   - Use `python -m build` and inspect the archive

3. **Import errors**:
   - Test the package in a fresh virtual environment
   - Check dependencies in pyproject.toml

### Rollback

If you need to remove a version:
- PyPI doesn't allow deletion of releases
- You can only "yank" releases (hide from pip install)
- Upload a new version with fixes

## Resources

- [PyPI Documentation](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [setuptools Documentation](https://setuptools.pypa.io/)